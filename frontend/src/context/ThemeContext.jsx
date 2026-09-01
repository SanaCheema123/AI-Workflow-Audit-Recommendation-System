import {
  createContext,
  useContext,
  useEffect,
  useMemo,
  useState,
} from 'react';

const ThemeContext = createContext(null);

export const accents = {
  pink: {
    name: 'Pink',
    deep: '#A55166',
    primary: '#D85C80',
    secondary: '#D38C9D',
    soft: '#E2B4C1',
    pale: '#F7DAE7',
    page: '#FFF7FA',
    card: '#FFFFFF',
    sidebar: '#5F1F35',
    sidebarDeep: '#250914',
    glow: '#D85C80',
  },

  rose: {
    name: 'Rose',
    deep: '#9D4960',
    primary: '#D96883',
    secondary: '#E49AAA',
    soft: '#F0BDC9',
    pale: '#FBE4EA',
    page: '#FFF8FA',
    card: '#FFFFFF',
    sidebar: '#733246',
    sidebarDeep: '#2A1018',
    glow: '#D96883',
  },

  purple: {
    name: 'Purple',
    deep: '#62417D',
    primary: '#8E63B6',
    secondary: '#AD87CC',
    soft: '#D5BDE5',
    pale: '#F1E7F7',
    page: '#FBF8FE',
    card: '#FFFFFF',
    sidebar: '#4E3565',
    sidebarDeep: '#1F1428',
    glow: '#8E63B6',
  },

  lavender: {
    name: 'Lavender',
    deep: '#75669B',
    primary: '#9788C1',
    secondary: '#B6A8D7',
    soft: '#D9D1EB',
    pale: '#F2EFF9',
    page: '#FBFAFE',
    card: '#FFFFFF',
    sidebar: '#51466E',
    sidebarDeep: '#211C2D',
    glow: '#9788C1',
  },

  blue: {
    name: 'Blue',
    deep: '#315E8C',
    primary: '#4F87C6',
    secondary: '#78A9DC',
    soft: '#B7D3EC',
    pale: '#E5F1FA',
    page: '#F7FBFF',
    card: '#FFFFFF',
    sidebar: '#294F74',
    sidebarDeep: '#102031',
    glow: '#4F87C6',
  },

  skyBlue: {
    name: 'Sky Blue',
    deep: '#3D7793',
    primary: '#62A6C8',
    secondary: '#8AC3DC',
    soft: '#C0E1EE',
    pale: '#E9F7FC',
    page: '#F6FCFF',
    card: '#FFFFFF',
    sidebar: '#336479',
    sidebarDeep: '#142A33',
    glow: '#62A6C8',
  },

  green: {
    name: 'Green',
    deep: '#3E7355',
    primary: '#5E9F74',
    secondary: '#86BE96',
    soft: '#B9D8C1',
    pale: '#E8F4EB',
    page: '#F7FCF8',
    card: '#FFFFFF',
    sidebar: '#315D45',
    sidebarDeep: '#14271D',
    glow: '#5E9F74',
  },

  seaGreen: {
    name: 'Sea Green',
    deep: '#286F69',
    primary: '#43988F',
    secondary: '#73BBB2',
    soft: '#AFD8D3',
    pale: '#E1F2F0',
    page: '#F5FCFB',
    card: '#FFFFFF',
    sidebar: '#235E59',
    sidebarDeep: '#102825',
    glow: '#43988F',
  },

  mint: {
    name: 'Mint',
    deep: '#4B806F',
    primary: '#71AD96',
    secondary: '#9CC8B8',
    soft: '#C8E2D8',
    pale: '#ECF7F2',
    page: '#F8FDFB',
    card: '#FFFFFF',
    sidebar: '#3B6759',
    sidebarDeep: '#182A24',
    glow: '#71AD96',
  },

  yellow: {
    name: 'Pastel Yellow',
    deep: '#977B38',
    primary: '#C6A450',
    secondary: '#DBC273',
    soft: '#ECDDAB',
    pale: '#FBF4D8',
    page: '#FFFDF5',
    card: '#FFFFFF',
    sidebar: '#78612D',
    sidebarDeep: '#2A220F',
    glow: '#C6A450',
  },

  peach: {
    name: 'Peach',
    deep: '#A86452',
    primary: '#D7856D',
    secondary: '#E5A895',
    soft: '#F0C8BA',
    pale: '#FAE9E3',
    page: '#FFF9F7',
    card: '#FFFFFF',
    sidebar: '#7C4A3D',
    sidebarDeep: '#2B1A15',
    glow: '#D7856D',
  },

  orange: {
    name: 'Pastel Orange',
    deep: '#A75F35',
    primary: '#D48855',
    secondary: '#E5A879',
    soft: '#F0C9A9',
    pale: '#FAEBDD',
    page: '#FFFAF6',
    card: '#FFFFFF',
    sidebar: '#774329',
    sidebarDeep: '#29180F',
    glow: '#D48855',
  },

  maroon: {
    name: 'Maroon',
    deep: '#4B1523',
    primary: '#761F37',
    secondary: '#A55166',
    soft: '#D8A1AF',
    pale: '#F4DDE3',
    page: '#FFF8FA',
    card: '#FFFFFF',
    sidebar: '#461321',
    sidebarDeep: '#1A070D',
    glow: '#A55166',
  },

  burgundy: {
    name: 'Burgundy',
    deep: '#36101C',
    primary: '#631E34',
    secondary: '#913F59',
    soft: '#C78B9D',
    pale: '#EDD4DC',
    page: '#FFF8FA',
    card: '#FFFFFF',
    sidebar: '#32101B',
    sidebarDeep: '#14070C',
    glow: '#913F59',
  },

  graphite: {
    name: 'Graphite',
    deep: '#19191D',
    primary: '#34343A',
    secondary: '#5B5B64',
    soft: '#B2B2BB',
    pale: '#ECECEF',
    page: '#F8F8F9',
    card: '#FFFFFF',
    sidebar: '#1B1B20',
    sidebarDeep: '#0D0D10',
    glow: '#5B5B64',
  },
};

export function ThemeProvider({ children }) {
  const [mode, setModeState] = useState(
    () => localStorage.getItem('audit-theme-mode') || 'light'
  );

  const [accent, setAccentState] = useState(
    () => localStorage.getItem('audit-accent') || 'maroon'
  );

  const [compact, setCompactState] = useState(
    () => localStorage.getItem('audit-compact') === 'true'
  );

  const setMode = (value) => {
    setModeState(value);
    localStorage.setItem('audit-theme-mode', value);
  };

  const setAccent = (value) => {
    if (!accents[value]) return;

    setAccentState(value);
    localStorage.setItem('audit-accent', value);
  };

  const setCompact = (value) => {
    setCompactState(value);
    localStorage.setItem('audit-compact', String(value));
  };

  useEffect(() => {
    const root = document.documentElement;

    root.dataset.theme = mode;
    root.dataset.accent = accent;

    if (compact) {
      root.dataset.compact = 'true';
    } else {
      delete root.dataset.compact;
    }
  }, [mode, compact, accent]);

  useEffect(() => {
    const palette = accents[accent] || accents.maroon;
    const root = document.documentElement;

    root.style.setProperty('--theme-deep', palette.deep);
    root.style.setProperty('--theme-primary', palette.primary);
    root.style.setProperty('--theme-secondary', palette.secondary);
    root.style.setProperty('--theme-soft', palette.soft);
    root.style.setProperty('--theme-pale', palette.pale);

    root.style.setProperty('--theme-page', palette.page);
    root.style.setProperty('--theme-card', palette.card);

    root.style.setProperty('--theme-sidebar', palette.sidebar);
    root.style.setProperty('--theme-sidebar-deep', palette.sidebarDeep);

    root.style.setProperty('--theme-glow', palette.glow);

    /*
      Compatibility aliases.

      If some of your existing CSS still uses old variable names,
      these will also change automatically.
    */

    root.style.setProperty('--accent-deep', palette.deep);
    root.style.setProperty('--accent-primary', palette.primary);
    root.style.setProperty('--accent-secondary', palette.secondary);
    root.style.setProperty('--accent-soft', palette.soft);
    root.style.setProperty('--accent-pale', palette.pale);

    root.style.setProperty('--primary', palette.primary);
    root.style.setProperty('--primary-dark', palette.deep);

    root.style.setProperty('--wine', palette.deep);
    root.style.setProperty('--rose', palette.primary);
    root.style.setProperty('--blush', palette.soft);
    root.style.setProperty('--pale', palette.pale);
  }, [accent]);

  const value = useMemo(
    () => ({
      mode,
      setMode,
      accent,
      setAccent,
      compact,
      setCompact,
      accents,
      currentAccent: accents[accent] || accents.maroon,
    }),
    [mode, accent, compact]
  );

  return (
    <ThemeContext.Provider value={value}>
      {children}
    </ThemeContext.Provider>
  );
}

export function useTheme() {
  const context = useContext(ThemeContext);

  if (!context) {
    throw new Error('useTheme must be used inside ThemeProvider');
  }

  return context;
}