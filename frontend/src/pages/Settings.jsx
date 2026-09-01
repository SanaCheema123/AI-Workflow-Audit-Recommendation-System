import { useEffect, useState } from 'react';
import {
  Bell,
  Check,
  Database,
  Moon,
  Palette,
  RefreshCcw,
  Server,
  SlidersHorizontal,
  Sun,
  Sparkles,
} from 'lucide-react';

import { useTheme } from '../context/ThemeContext';
import { api, API_BASE_URL } from '../lib/api';
import Toast from '../components/Toast';

export default function Settings() {
  const {
    mode,
    setMode,
    accent,
    setAccent,
    compact,
    setCompact,
    accents,
  } = useTheme();

  const [health, setHealth] = useState(null);

  const [autoRefresh, setAutoRefresh] = useState(
    () => localStorage.getItem('audit-auto-refresh') !== 'false'
  );

  const [notifications, setNotifications] = useState(
    () => localStorage.getItem('audit-notifications') !== 'false'
  );

  const [toast, setToast] = useState(null);

  useEffect(() => {
    api
      .health()
      .then(setHealth)
      .catch(() => setHealth(null));
  }, []);

  const saveBool = (key, setter, value) => {
    setter(value);
    localStorage.setItem(key, String(value));

    setToast({
      message: 'Preference saved.',
    });
  };

  const handleModeChange = (newMode) => {
    setMode(newMode);

    setToast({
      message:
        newMode === 'light'
          ? 'Light workspace enabled. Sidebar remains dark.'
          : 'Dark workspace enabled.',
    });
  };

  const handleAccentChange = (key) => {
    setAccent(key);

    const selectedPalette = accents[key];

    setToast({
      message: `${selectedPalette?.name || 'Accent'} theme applied.`,
    });
  };

  const refreshConnection = () => {
    api
      .health()
      .then((response) => {
        setHealth(response);

        setToast({
          message: 'Connection refreshed.',
        });
      })
      .catch((error) => {
        setHealth(null);

        setToast({
          type: 'error',
          message: error.message,
        });
      });
  };

  return (
    <div className="settings-grid">
      <Toast toast={toast} onClose={() => setToast(null)} />

      {/* =========================
          MAIN SETTINGS AREA
      ========================== */}
      <section className="panel settings-main">

        {/* =========================
            APPEARANCE MODE
        ========================== */}
        <div className="settings-section">
          <div className="section-title">
            <span className="feature-icon">
              <Moon />
            </span>

            <div>
              <h2>Appearance mode</h2>
              <p>
                Change the workspace appearance while keeping your sidebar
                permanently dark.
              </p>
            </div>
          </div>

          <div className="mode-choice">

            {/* LIGHT MODE */}
            <button
              type="button"
              className={mode === 'light' ? 'active' : ''}
              onClick={() => handleModeChange('light')}
            >
              <span className="mode-choice-icon">
                <Sun />
              </span>

              <span className="mode-choice-content">
                <b>Light</b>
                <span>Bright workspace with dark sidebar</span>
              </span>

              {mode === 'light' && (
                <span className="mode-check">
                  <Check size={18} />
                </span>
              )}
            </button>

            {/* DARK MODE */}
            <button
              type="button"
              className={mode === 'dark' ? 'active' : ''}
              onClick={() => handleModeChange('dark')}
            >
              <span className="mode-choice-icon">
                <Moon />
              </span>

              <span className="mode-choice-content">
                <b>Dark</b>
                <span>Deep dark workspace and sidebar</span>
              </span>

              {mode === 'dark' && (
                <span className="mode-check">
                  <Check size={18} />
                </span>
              )}
            </button>
          </div>
        </div>

        {/* =========================
            ACCENT PALETTE
        ========================== */}
        <div className="settings-section">
          <div className="section-title">
            <span className="feature-icon">
              <Palette />
            </span>

            <div>
              <h2>Accent palette</h2>
              <p>
                Select a pastel or deep accent theme. Your selection is applied
                across the complete application.
              </p>
            </div>
          </div>

          <div className="palette-grid">
            {Object.entries(accents).map(([key, palette]) => {
              const selected = accent === key;

              return (
                <button
                  type="button"
                  key={key}
                  className={`palette-card ${selected ? 'active' : ''}`}
                  onClick={() => handleAccentChange(key)}
                  aria-pressed={selected}
                  title={`Apply ${palette.name} theme`}
                >
                  <span className="swatches">
                    <i
                      style={{
                        background: palette.deep,
                      }}
                    />

                    <i
                      style={{
                        background: palette.primary,
                      }}
                    />

                    <i
                      style={{
                        background: palette.secondary,
                      }}
                    />

                    <i
                      style={{
                        background: palette.soft,
                      }}
                    />

                    <i
                      style={{
                        background: palette.pale,
                      }}
                    />
                  </span>

                  <span className="palette-info">
                    <b>{palette.name}</b>

                    {selected && (
                      <span className="palette-selected">
                        <Check size={15} />
                        Selected
                      </span>
                    )}
                  </span>
                </button>
              );
            })}
          </div>
        </div>

        {/* =========================
            WORKSPACE BEHAVIOR
        ========================== */}
        <div className="settings-section">
          <div className="section-title">
            <span className="feature-icon">
              <SlidersHorizontal />
            </span>

            <div>
              <h2>Workspace behavior</h2>
              <p>
                Manage interface preferences stored locally in this browser.
              </p>
            </div>
          </div>

          <SettingToggle
            icon={RefreshCcw}
            title="Auto-refresh audit views"
            desc="Keep portfolio data fresh when you revisit a page."
            checked={autoRefresh}
            onChange={(value) =>
              saveBool(
                'audit-auto-refresh',
                setAutoRefresh,
                value
              )
            }
          />

          <SettingToggle
            icon={Bell}
            title="Interface notifications"
            desc="Show in-app confirmations for audit actions."
            checked={notifications}
            onChange={(value) =>
              saveBool(
                'audit-notifications',
                setNotifications,
                value
              )
            }
          />

          <SettingToggle
            icon={Database}
            title="Compact density"
            desc="Tighten cards and rows for dense audit portfolios."
            checked={compact}
            onChange={setCompact}
          />
        </div>
      </section>

      {/* =========================
          RIGHT SETTINGS COLUMN
      ========================== */}
      <aside className="settings-side">

        {/* BACKEND CONNECTION */}
        <section className="panel connection-card">
          <span className="feature-icon">
            <Server />
          </span>

          <p className="eyebrow">
            BACKEND CONNECTION
          </p>

          <h3>
            {health ? 'API operational' : 'API unavailable'}
          </h3>

          <p className="connection-url">
            {API_BASE_URL}
          </p>

          <div
            className={`connection-state ${
              health ? 'ok' : 'bad'
            }`}
          >
            <i />

            {health
              ? 'Health endpoint responded successfully'
              : 'Unable to reach /health'}
          </div>

          <button
            type="button"
            className="soft-btn"
            onClick={refreshConnection}
          >
            <RefreshCcw size={16} />
            Test connection
          </button>
        </section>

        {/* THEME INFORMATION */}
        <section className="panel note-card">
          <span className="feature-icon">
            <Sparkles />
          </span>

          <h3>Global appearance</h3>

          <p>
            Light and dark modes affect your workspace only.
            The navigation sidebar stays dark for visual consistency.
          </p>

          <p>
            Accent palettes update interactive elements throughout
            Dashboard, Audits, New Audit, Settings and the landing
            experience.
          </p>
        </section>

        {/* BACKEND NOTE */}
        <section className="panel note-card">
          <h3>Backend-aware settings</h3>

          <p>
            Your backend currently exposes audit and health APIs.
            Appearance preferences are stored locally instead of
            creating unsupported backend endpoints.
          </p>
        </section>
      </aside>
    </div>
  );
}

/* =====================================================
   REUSABLE SETTINGS TOGGLE
===================================================== */

function SettingToggle({
  icon: Icon,
  title,
  desc,
  checked,
  onChange,
}) {
  return (
    <button
      type="button"
      className="setting-row"
      onClick={() => onChange(!checked)}
      aria-pressed={checked}
    >
      <span className="setting-icon">
        <Icon size={18} />
      </span>

      <span className="grow">
        <b>{title}</b>
        <small>{desc}</small>
      </span>

      <span className={`toggle ${checked ? 'on' : ''}`}>
        <i />
      </span>
    </button>
  );
}