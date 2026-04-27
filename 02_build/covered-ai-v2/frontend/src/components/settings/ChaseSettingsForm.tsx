'use client';

import { useState } from 'react';
import { Bell, Loader2 } from 'lucide-react';
import { Button } from '@/components/ui';
import { cn } from '@/lib/utils';

interface ChaseSettings {
  autoChaseEnabled: boolean;
  reminder1Days: number;
  reminder2Days: number;
  reminder3Days: number;
}

interface ChaseSettingsFormProps {
  initialSettings: ChaseSettings;
  onSave: (settings: ChaseSettings) => Promise<void>;
}

export function ChaseSettingsForm({ initialSettings, onSave }: ChaseSettingsFormProps) {
  const [settings, setSettings] = useState<ChaseSettings>(initialSettings);
  const [isSaving, setIsSaving] = useState(false);
  const [saved, setSaved] = useState(false);

  const handleToggle = () => {
    setSettings((prev) => ({ ...prev, autoChaseEnabled: !prev.autoChaseEnabled }));
    setSaved(false);
  };

  const handleDaysChange = (field: 'reminder1Days' | 'reminder2Days' | 'reminder3Days', value: number) => {
    setSettings((prev) => ({ ...prev, [field]: value }));
    setSaved(false);
  };

  const handleSave = async () => {
    setIsSaving(true);
    try {
      await onSave(settings);
      setSaved(true);
      setTimeout(() => setSaved(false), 3000);
    } catch (err) {
      console.error('Failed to save chase settings:', err);
    } finally {
      setIsSaving(false);
    }
  };

  return (
    <div className="bg-white rounded-xl border border-[var(--grey-200)] overflow-hidden">
      {/* Header */}
      <div className="p-4 border-b border-[var(--grey-200)]">
        <div className="flex items-center gap-3">
          <div className="w-10 h-10 bg-amber-100 rounded-lg flex items-center justify-center">
            <Bell className="w-5 h-5 text-amber-600" />
          </div>
          <div>
            <h3 className="font-semibold text-[var(--grey-900)]">Auto-Chase</h3>
            <p className="text-sm text-[var(--grey-500)]">
              Automatic payment reminders for overdue invoices
            </p>
          </div>
        </div>
      </div>

      {/* Toggle */}
      <div className="p-4 border-b border-[var(--grey-200)]">
        <div className="flex items-center justify-between">
          <div>
            <p className="font-medium text-[var(--grey-900)]">Enable Auto-Chase</p>
            <p className="text-sm text-[var(--grey-500)]">
              Automatically send payment reminders when invoices become overdue
            </p>
          </div>
          <button
            onClick={handleToggle}
            className={cn(
              'relative w-12 h-6 rounded-full transition-colors',
              settings.autoChaseEnabled ? 'bg-[var(--brand-primary)]' : 'bg-[var(--grey-300)]'
            )}
          >
            <span
              className={cn(
                'absolute top-1 w-4 h-4 bg-white rounded-full transition-transform shadow-sm',
                settings.autoChaseEnabled ? 'translate-x-7' : 'translate-x-1'
              )}
            />
          </button>
        </div>
      </div>

      {/* Reminder Settings */}
      <div className={cn('p-4 space-y-4', !settings.autoChaseEnabled && 'opacity-50')}>
        <p className="text-sm font-medium text-[var(--grey-700)]">
          Send reminders at these intervals after the due date:
        </p>

        {/* Reminder 1 */}
        <div className="flex items-center gap-4">
          <div className="flex-1">
            <label className="text-sm text-[var(--grey-600)]">First Reminder (Friendly)</label>
          </div>
          <div className="flex items-center gap-2">
            <input
              type="number"
              min={1}
              max={30}
              value={settings.reminder1Days}
              onChange={(e) => handleDaysChange('reminder1Days', parseInt(e.target.value) || 7)}
              disabled={!settings.autoChaseEnabled}
              className="w-16 px-3 py-2 border border-[var(--grey-200)] rounded-lg text-center text-sm disabled:opacity-50"
            />
            <span className="text-sm text-[var(--grey-500)]">days</span>
          </div>
        </div>

        {/* Reminder 2 */}
        <div className="flex items-center gap-4">
          <div className="flex-1">
            <label className="text-sm text-[var(--grey-600)]">Second Reminder (Firm)</label>
          </div>
          <div className="flex items-center gap-2">
            <input
              type="number"
              min={1}
              max={30}
              value={settings.reminder2Days}
              onChange={(e) => handleDaysChange('reminder2Days', parseInt(e.target.value) || 14)}
              disabled={!settings.autoChaseEnabled}
              className="w-16 px-3 py-2 border border-[var(--grey-200)] rounded-lg text-center text-sm disabled:opacity-50"
            />
            <span className="text-sm text-[var(--grey-500)]">days</span>
          </div>
        </div>

        {/* Reminder 3 / Final Notice */}
        <div className="flex items-center gap-4">
          <div className="flex-1">
            <label className="text-sm text-[var(--grey-600)]">Final Notice (Urgent)</label>
          </div>
          <div className="flex items-center gap-2">
            <input
              type="number"
              min={1}
              max={60}
              value={settings.reminder3Days}
              onChange={(e) => handleDaysChange('reminder3Days', parseInt(e.target.value) || 21)}
              disabled={!settings.autoChaseEnabled}
              className="w-16 px-3 py-2 border border-[var(--grey-200)] rounded-lg text-center text-sm disabled:opacity-50"
            />
            <span className="text-sm text-[var(--grey-500)]">days</span>
          </div>
        </div>

        {/* Preview Timeline */}
        <div className="bg-[var(--grey-50)] rounded-lg p-3 mt-4">
          <p className="text-xs font-medium text-[var(--grey-600)] mb-2">Preview</p>
          <div className="flex items-center text-xs text-[var(--grey-500)]">
            <span>Due Date</span>
            <span className="mx-2">→</span>
            <span className="text-green-600">+{settings.reminder1Days}d: Friendly</span>
            <span className="mx-2">→</span>
            <span className="text-amber-600">+{settings.reminder2Days}d: Firm</span>
            <span className="mx-2">→</span>
            <span className="text-red-600">+{settings.reminder3Days}d: Final</span>
          </div>
        </div>
      </div>

      {/* Save Button */}
      <div className="p-4 border-t border-[var(--grey-200)] bg-[var(--grey-50)]">
        <Button
          onClick={handleSave}
          disabled={isSaving}
          className="w-full"
        >
          {isSaving ? (
            <>
              <Loader2 className="w-4 h-4 animate-spin mr-2" />
              Saving...
            </>
          ) : saved ? (
            'Saved!'
          ) : (
            'Save Changes'
          )}
        </Button>
      </div>
    </div>
  );
}

export default ChaseSettingsForm;
