// Renders a placeholder "two eyes staring" clip so the site is real before the
// generated video exists. Everything is periodic over DUR, so `<video loop>`
// has no visible seam -- which also proves the loop path end to end.
import { spawn } from 'node:child_process';

const W = 1280, H = 720, FPS = 25, DUR = 12, N = FPS * DUR;
const OUT = process.argv[2] ?? 'public/eye.mp4';

const clamp = (v, a, b) => (v < a ? a : v > b ? b : v);
const mix = (a, b, t) => a + (b - a) * t;
const smoothstep = (e0, e1, x) => { const t = clamp((x - e0) / (e1 - e0), 0, 1); return t * t * (3 - 2 * t); };

function hash2(x, y) { const n = Math.sin(x * 127.1 + y * 311.7) * 43758.5453; return n - Math.floor(n); }
function vnoise(x, y) {
  const xi = Math.floor(x), yi = Math.floor(y), xf = x - xi, yf = y - yi;
  const u = xf * xf * (3 - 2 * xf), v = yf * yf * (3 - 2 * yf);
  const a = hash2(xi, yi), b = hash2(xi + 1, yi), c = hash2(xi, yi + 1), d = hash2(xi + 1, yi + 1);
  return a + (b - a) * u + (c - a) * v + (a - b - c + d) * u * v;
}

// Blinks placed away from t=0 and t=DUR so the loop point stays open-eyed.
const BLINKS = [3.0, 8.6];
function blinkAmount(t) {
  let m = 0;
  for (const b of BLINKS) {
    const d = t - b;
    if (d < -0.02 || d > 0.30) continue;
    let a;
    if (d < 0.10) a = smoothstep(0, 0.10, d);          // close
    else if (d < 0.14) a = 1;                           // held shut
    else a = 1 - smoothstep(0.14, 0.30, d);             // open
    m = Math.max(m, a);
  }
  return m;
}

const EYES = [
  { cx: W * 0.315, cy: H * 0.50, hw: W * 0.150, hh: H * 0.128 },
  { cx: W * 0.685, cy: H * 0.50, hw: W * 0.150, hh: H * 0.128 },
];
const BG = [6, 6, 7];

const frame = Buffer.alloc(W * H * 3);
const ff = spawn('ffmpeg', [
  '-y', '-f', 'rawvideo', '-pix_fmt', 'rgb24', '-s', `${W}x${H}`, '-r', String(FPS),
  '-i', 'pipe:0',
  '-an', '-c:v', 'libx264', '-preset', 'slow', '-crf', '20',
  '-profile:v', 'high', '-pix_fmt', 'yuv420p', '-movflags', '+faststart',
  OUT,
], { stdio: ['pipe', 'inherit', 'inherit'] });

const write = (buf) => new Promise((res) => { if (!ff.stdin.write(buf)) ff.stdin.once('drain', res); else res(); });

for (let f = 0; f < N; f++) {
  const t = f / FPS;

  // background + grain
  for (let i = 0, p = 0; i < W * H; i++) {
    const g = (hash2(i % W + f * 7, (i / W) | 0) - 0.5) * 5;
    frame[p++] = clamp(BG[0] + g, 0, 255);
    frame[p++] = clamp(BG[1] + g, 0, 255);
    frame[p++] = clamp(BG[2] + g, 0, 255);
  }

  const blink = blinkAmount(t);
  // hippus: slow involuntary pupil oscillation, periodic over 6s -> loops at 12s
  const pr = 0.300 + 0.038 * Math.sin((2 * Math.PI * t) / 6) + 0.016 * Math.sin((2 * Math.PI * t) / 3 + 1.1);

  for (const e of EYES) {
    const R = e.hh * 1.15;                 // iris radius vs. palpebral height, roughly anatomical
    const A = 1.0, B = 0.86;               // upper / lower lid extents
    const x0 = Math.max(0, (e.cx - e.hw - 8) | 0), x1 = Math.min(W - 1, (e.cx + e.hw + 8) | 0);
    const y0 = Math.max(0, (e.cy - e.hh - 10) | 0), y1 = Math.min(H - 1, (e.cy + e.hh + 10) | 0);

    for (let y = y0; y <= y1; y++) {
      for (let x = x0; x <= x1; x++) {
        const u = (x - e.cx) / e.hw;
        if (u <= -1 || u >= 1) continue;
        const v = (y - e.cy) / e.hh;
        const s = Math.pow(1 - u * u, 0.70);
        const yTop = (-A + blink * (A + B)) * s;
        const yBot = B * s;
        if (v <= yTop || v >= yBot) continue;

        const edge = Math.min(smoothstep(0, 0.10, v - yTop), smoothstep(0, 0.09, yBot - v));
        if (edge <= 0) continue;

        // sclera, shaded by lid shadow above and vessel wash at the corners
        const lidShade = mix(0.58, 1.0, smoothstep(0, 0.55, v - yTop));
        const corner = smoothstep(0.55, 1.0, Math.abs(u));
        const vessels = vnoise(x * 0.05 + 40, y * 0.16) * corner * 0.30;
        let r = 236 * lidShade, g = 231 * lidShade, b = 227 * lidShade;
        r = mix(r, 196, vessels); g = mix(g, 150, vessels); b = mix(b, 146, vessels);

        const dx = x - e.cx, dy = y - e.cy;
        const d = Math.hypot(dx, dy);
        const rn = d / R;

        if (rn < 1.02) {
          const ang = Math.atan2(dy, dx);
          const fib = vnoise(ang * 26, rn * 9) * 0.66 + vnoise(ang * 78, rn * 22) * 0.34;
          const tOut = smoothstep(0.30, 0.95, rn);
          let ir = mix(150, 78, tOut), ig = mix(112, 100, tOut), ib = mix(62, 126, tOut);
          const k = 0.72 + fib * 0.56;
          ir *= k; ig *= k; ib *= k;

          // collarette, then the dark limbal ring at the outer edge
          const col = Math.exp(-Math.pow((rn - 0.44) / 0.06, 2)) * 0.30;
          ir = mix(ir, ir * 1.5 + 24, col); ig = mix(ig, ig * 1.5 + 20, col); ib = mix(ib, ib * 1.4 + 16, col);
          const limb = smoothstep(0.86, 1.0, rn);
          ir = mix(ir, 16, limb); ig = mix(ig, 18, limb); ib = mix(ib, 24, limb);

          const pupil = 1 - smoothstep(pr - 0.02, pr + 0.02, rn);
          ir = mix(ir, 5, pupil); ig = mix(ig, 5, pupil); ib = mix(ib, 7, pupil);

          const irisMask = 1 - smoothstep(0.985, 1.02, rn);
          r = mix(r, ir, irisMask); g = mix(g, ig, irisMask); b = mix(b, ib, irisMask);

          // shadow the top of the globe under the upper lid
          const sh = (1 - smoothstep(0, 0.7, v - yTop)) * 0.42;
          r *= 1 - sh; g *= 1 - sh; b *= 1 - sh;
        }

        // wet specular: one dominant catchlight, one faint bounce
        const h1 = Math.exp(-(Math.pow(dx + 0.34 * R, 2) + Math.pow(dy + 0.40 * R, 2)) / (2 * Math.pow(0.155 * R, 2)));
        const h2 = Math.exp(-(Math.pow(dx - 0.30 * R, 2) + Math.pow(dy - 0.26 * R, 2)) / (2 * Math.pow(0.085 * R, 2))) * 0.32;
        const hl = clamp(h1 + h2, 0, 1);
        r = mix(r, 255, hl); g = mix(g, 255, hl); b = mix(b, 254, hl);

        // lid line: eyes float out of black rather than sit in a badly-drawn face
        r = mix(BG[0], r, edge); g = mix(BG[1], g, edge); b = mix(BG[2], b, edge);

        const p = (y * W + x) * 3;
        frame[p] = clamp(r, 0, 255);
        frame[p + 1] = clamp(g, 0, 255);
        frame[p + 2] = clamp(b, 0, 255);
      }
    }
  }

  await write(Buffer.from(frame));
  if (f % 25 === 0) process.stderr.write(`\rframe ${f}/${N}`);
}

ff.stdin.end();
await new Promise((res, rej) => ff.on('close', (c) => (c === 0 ? res() : rej(new Error('ffmpeg exit ' + c)))));
process.stderr.write('\rdone            \n');
