import React from 'react';
import {AbsoluteFill, interpolate, useCurrentFrame, Easing} from 'remotion';

const PAPER = '#F7F3EA';
const PAPER2 = '#F0EADC';
const INK = '#1C1710';
const MUTED = '#6E6659';
const RULE = '#D8D0C0';
const ACCENT = '#C93D1B';
const SERIF = 'Georgia, "Times New Roman", serif';
const MONO = 'Consolas, "Courier New", monospace';

const clamp = {extrapolateLeft: 'clamp', extrapolateRight: 'clamp'} as const;

// Fade + rise into place over ~14 frames starting at `at`.
const useRise = (at: number, dist = 26) => {
  const f = useCurrentFrame();
  const t = interpolate(f, [at, at + 14], [0, 1], {...clamp, easing: Easing.out(Easing.cubic)});
  return {opacity: t, transform: `translateY(${(1 - t) * dist}px)`};
};

// Rubber-stamp: drops in with a slight overshoot scale.
const useStamp = (at: number) => {
  const f = useCurrentFrame();
  const t = interpolate(f, [at, at + 8], [0, 1], {...clamp, easing: Easing.out(Easing.quad)});
  const s = interpolate(f, [at, at + 8], [1.6, 1], {...clamp, easing: Easing.out(Easing.back(1.6))});
  return {opacity: t, transform: `scale(${s})`};
};

const useFadeWindow = (start: number, end: number) => {
  const f = useCurrentFrame();
  return interpolate(f, [start, start + 10, end - 10, end], [0, 1, 1, 0], clamp);
};

const Beat: React.FC<{start: number; end: number; children: React.ReactNode}> = ({start, end, children}) => {
  const f = useCurrentFrame();
  const opacity = useFadeWindow(start, end);
  if (f < start - 2 || f > end + 2) return null;
  return <AbsoluteFill style={{opacity}}>{children}</AbsoluteFill>;
};

const Center: React.FC<{children: React.ReactNode}> = ({children}) => (
  <AbsoluteFill style={{justifyContent: 'center', alignItems: 'center', padding: 140}}>
    <div style={{width: '100%', maxWidth: 1460}}>{children}</div>
  </AbsoluteFill>
);

// ---- Beat 3 terminal helpers ------------------------------------------------
const TERMINAL_LINES: Array<{text: string; who: 'cmd' | 'q' | 'a' | 'est'; at: number}> = [
  {text: '$ metaharness run website', who: 'cmd', at: 260},
  {text: 'Single page or multi-page?', who: 'q', at: 300},
  {text: '> multi-page (3-8 pages)', who: 'a', at: 322},
  {text: 'Copy: have it, or agent writes it?', who: 'q', at: 344},
  {text: '> agent writes it', who: 'a', at: 366},
  {text: 'composing harness... skills, runbook, loops, gates', who: 'q', at: 392},
  {text: 'budget ≈ 2-8% of a Max 20x week', who: 'est', at: 420},
];

const TerminalLine: React.FC<{line: (typeof TERMINAL_LINES)[number]}> = ({line}) => {
  const f = useCurrentFrame();
  const stamp = useStamp(line.at);
  if (f < line.at) return null;
  const chars = Math.floor((f - line.at) * 2.2);
  const shown = line.who === 'cmd' ? line.text.slice(0, chars) : line.text;
  const style: React.CSSProperties = {
    fontFamily: MONO, fontSize: 34, lineHeight: 1.9,
    color: line.who === 'a' ? '#EAD9B0' : line.who === 'est' ? PAPER : '#B9AE9C',
  };
  if (line.who === 'cmd') style.color = PAPER;
  if (line.who === 'est') {
    return (
      <div style={{...style, ...stamp}}>
        <span style={{background: ACCENT, color: PAPER, padding: '6px 18px'}}>{shown}</span>
      </div>
    );
  }
  return <div style={style}>{shown}{line.who === 'cmd' && chars < line.text.length ? '▋' : ''}</div>;
};

// ---- Beat 4 index rows ------------------------------------------------------
const ROWS = [
  {no: '01', name: 'anthropics/skills: frontend-design', why: 'kills the generic AI aesthetic at the source', score: '10'},
  {no: '02', name: 'playwright MCP', why: 'gives the agent eyes; every design loop depends on it', score: '10'},
  {no: '03', name: 'obra/superpowers', why: 'verification-before-completion, as an install', score: '9'},
];

const IndexRow: React.FC<{row: (typeof ROWS)[number]; at: number}> = ({row, at}) => (
  <div style={{
    display: 'grid', gridTemplateColumns: '90px 1fr 150px', alignItems: 'baseline',
    padding: '34px 10px', borderBottom: `1px solid ${RULE}`, ...useRise(at),
  }}>
    <div style={{fontFamily: MONO, fontSize: 26, color: MUTED}}>{row.no}</div>
    <div>
      <div style={{fontFamily: SERIF, fontSize: 40, fontWeight: 600, color: INK}}>{row.name}</div>
      <div style={{fontFamily: SERIF, fontSize: 28, color: MUTED, marginTop: 6}}>{row.why}</div>
    </div>
    <div style={{fontFamily: MONO, fontSize: 64, color: ACCENT, textAlign: 'right', ...useStamp(at + 10)}}>
      {row.score}<span style={{fontSize: 26, color: MUTED}}>/10</span>
    </div>
  </div>
);

// ---- The film ---------------------------------------------------------------
export const Promo: React.FC = () => {
  return (
    <AbsoluteFill style={{background: PAPER}}>

      {/* Beat 1: 0-105 */}
      <Beat start={0} end={105}>
        <Center>
          <div style={{fontFamily: SERIF, fontSize: 104, fontWeight: 600, lineHeight: 1.08, color: INK, maxWidth: 1250, ...useRise(6)}}>
            There is a layer between your prompt and great AI output.
          </div>
        </Center>
      </Beat>

      {/* Beat 2: 105-255 */}
      <Beat start={105} end={255}>
        <Center>
          <div style={{fontFamily: SERIF, fontSize: 84, fontWeight: 600, color: INK, ...useRise(112)}}>
            The harness around the model.
          </div>
          <div style={{marginTop: 70, borderTop: `2px solid ${INK}`, maxWidth: 1000}}>
            {['skills installed', 'iteration loops', 'verification gates'].map((t, i) => (
              <div key={t} style={{
                fontFamily: MONO, fontSize: 40, color: INK, padding: '26px 8px',
                borderBottom: `1px solid ${RULE}`, ...useRise(150 + i * 22),
              }}>{t}</div>
            ))}
          </div>
        </Center>
      </Beat>

      {/* Beat 3: 255-495 */}
      <Beat start={255} end={495}>
        <Center>
          <div style={{background: INK, borderRadius: 6, padding: '70px 80px', minHeight: 620, ...useRise(258, 40)}}>
            {TERMINAL_LINES.map((l) => <TerminalLine key={l.text} line={l} />)}
          </div>
        </Center>
      </Beat>

      {/* Beat 4: 495-645 */}
      <Beat start={495} end={645}>
        <Center>
          <div style={{fontFamily: SERIF, fontSize: 56, fontWeight: 600, color: INK, marginBottom: 30, ...useRise(500)}}>
            Composed from a rated index of the whole ecosystem.
            <span style={{color: ACCENT}}> Refreshed daily.</span>
          </div>
          <div style={{borderTop: `2px solid ${INK}`, background: PAPER2}}>
            {ROWS.map((r, i) => <IndexRow key={r.no} row={r} at={520 + i * 22} />)}
          </div>
        </Center>
      </Beat>

      {/* Beat 5: 645-810 */}
      <Beat start={645} end={810}>
        <Center>
          <div style={{fontFamily: SERIF, fontSize: 96, fontWeight: 600, lineHeight: 1.1, color: INK, maxWidth: 1350, ...useRise(652)}}>
            Give your AI the intuition of <span style={{color: ACCENT, fontStyle: 'italic'}}>the best in the world</span> at any task.
          </div>
          <div style={{fontFamily: MONO, fontSize: 38, color: MUTED, marginTop: 80, ...useRise(700)}}>
            github.com/prajval-kesireddy/meta-harness
          </div>
        </Center>
      </Beat>

    </AbsoluteFill>
  );
};
