---
title: "Covered AI — UI Component Reference"
id: "11-ui-component-reference"
version: 1
created: "2026-04-25"
type: "document"
topic_type: "unsorted"
audience: "internal"
layer: "shadow"
status: "filed"
signed_by: "Devon, 2026-04-25, devin-992682c244cf444f91e0a516498afbfd"
---

# Covered AI — UI Component Reference

## Document Info
- **Version**: 1.0
- **Created**: 2025-01-27
- **Purpose**: Exact HTML/Tailwind patterns for Claude Code to replicate
- **Reference**: See dashboard-mockup.html for live preview

---

# TAILWIND CONFIG

Add to `tailwind.config.js`:

```javascript
module.exports = {
  content: [
    './src/**/*.{js,ts,jsx,tsx,mdx}',
  ],
  theme: {
    extend: {
      fontFamily: {
        sans: ['Inter', 'system-ui', 'sans-serif'],
      },
      colors: {
        brand: {
          primary: '#2563eb',
          'primary-hover': '#1d4ed8',
          'primary-light': '#dbeafe',
        },
        grey: {
          50: '#f9fafb',
          100: '#f3f4f6',
          200: '#e5e7eb',
          300: '#d1d5db',
          400: '#9ca3af',
          500: '#6b7280',
          600: '#4b5563',
          700: '#374151',
          800: '#1f2937',
          900: '#111827',
        },
      },
    },
  },
  plugins: [],
}
```

Add to `globals.css`:

```css
@import url('https://fonts.googleapis.com/css2?family=Inter:wght@400;500;600;700&display=swap');

.tabular-nums {
  font-variant-numeric: tabular-nums;
}

.safe-area-pb {
  padding-bottom: max(12px, env(safe-area-inset-bottom));
}
```

---

# COMPONENT PATTERNS

## 1. Page Layout

```tsx
// src/components/layout/DashboardLayout.tsx

interface DashboardLayoutProps {
  children: React.ReactNode;
}

export function DashboardLayout({ children }: DashboardLayoutProps) {
  return (
    <div className="min-h-screen bg-grey-50">
      <div className="max-w-md mx-auto bg-white min-h-screen">
        {children}
        <BottomNavigation />
      </div>
    </div>
  );
}
```

## 2. Header

```tsx
// src/components/layout/Header.tsx

interface HeaderProps {
  greeting?: boolean;
  title: string;
  subtitle?: string;
  action?: React.ReactNode;
  backButton?: boolean;
  onBack?: () => void;
}

// Greeting header (dashboard)
<header className="bg-white border-b border-grey-200 px-4 py-3 sticky top-0 z-10">
  <div className="flex items-center justify-between">
    <div>
      <p className="text-sm text-grey-500">{greeting}</p>
      <h1 className="text-xl font-semibold text-grey-900">{name}</h1>
    </div>
    <div className="flex items-center gap-2">
      <IconButton icon={HelpIcon} />
      <IconButton icon={SettingsIcon} />
    </div>
  </div>
</header>

// Page header (invoices, etc)
<header className="bg-white border-b border-grey-200 px-4 py-3 sticky top-0 z-10">
  <div className="flex items-center justify-between">
    <h1 className="text-xl font-semibold text-grey-900">{title}</h1>
    {action}
  </div>
</header>

// Back header (forms)
<header className="bg-white border-b border-grey-200 px-4 py-3 flex items-center gap-3">
  <button 
    onClick={onBack}
    className="w-10 h-10 flex items-center justify-center text-grey-400 hover:text-grey-600 hover:bg-grey-100 rounded-lg transition-colors"
  >
    <ChevronLeftIcon className="w-5 h-5" />
  </button>
  <h1 className="text-xl font-semibold text-grey-900">{title}</h1>
</header>
```

## 3. Bottom Navigation

```tsx
// src/components/layout/BottomNavigation.tsx

const navItems = [
  { id: 'home', icon: HomeIcon, label: 'Home', href: '/dashboard' },
  { id: 'calls', icon: PhoneIcon, label: 'Calls', href: '/dashboard/calls' },
  { id: 'new', icon: PlusIcon, label: 'New', href: '/dashboard/new', primary: true },
  { id: 'invoices', icon: FileTextIcon, label: 'Invoices', href: '/dashboard/invoices' },
  { id: 'reports', icon: BarChartIcon, label: 'Reports', href: '/dashboard/reports' },
];

export function BottomNavigation() {
  const pathname = usePathname();
  
  return (
    <nav className="fixed bottom-0 left-0 right-0 max-w-md mx-auto bg-white border-t border-grey-200 px-4 py-2 safe-area-pb">
      <div className="flex items-center justify-around">
        {navItems.map((item) => (
          <Link
            key={item.id}
            href={item.href}
            className={cn(
              "flex flex-col items-center gap-1 px-4 py-2",
              item.primary 
                ? "rounded-xl bg-brand-primary text-white -mt-4 shadow-lg"
                : pathname === item.href
                  ? "text-brand-primary"
                  : "text-grey-400"
            )}
          >
            <item.icon className="w-6 h-6" />
            <span className="text-xs font-medium">{item.label}</span>
          </Link>
        ))}
      </div>
    </nav>
  );
}
```

## 4. Needs Attention Feed

```tsx
// src/components/dashboard/NeedsAttentionFeed.tsx

interface AttentionItem {
  id: string;
  type: 'emergency' | 'callback' | 'overdue' | 'review' | 'followup';
  title: string;
  subtitle: string;
  action: {
    label: string;
    variant: 'danger' | 'warning' | 'primary';
    onClick: () => void;
  };
}

const typeConfig = {
  emergency: { icon: '⚡', bgClass: 'bg-red-50/30' },
  callback: { icon: '📞', bgClass: '' },
  overdue: { icon: '💷', bgClass: '' },
  review: { icon: '⭐', bgClass: '' },
  followup: { icon: '📋', bgClass: '' },
};

const actionVariants = {
  danger: 'bg-red-600 hover:bg-red-700 text-white',
  warning: 'bg-amber-500 hover:bg-amber-600 text-white',
  primary: 'bg-brand-primary hover:bg-brand-primary-hover text-white',
};

// All clear state
function AllClearState() {
  return (
    <section className="bg-green-50 rounded-xl border border-green-200 p-6 text-center">
      <span className="text-5xl">✓</span>
      <h2 className="mt-3 text-lg font-semibold text-green-900">All clear</h2>
      <p className="text-sm text-green-700 mt-1">Nothing needs your attention right now</p>
    </section>
  );
}

// Feed with items
export function NeedsAttentionFeed({ items }: { items: AttentionItem[] }) {
  if (items.length === 0) return <AllClearState />;

  return (
    <section className="bg-white rounded-xl border border-grey-200 overflow-hidden shadow-sm">
      {/* Header */}
      <div className="px-4 py-3 bg-red-50 border-b border-red-100">
        <div className="flex items-center gap-2">
          <span className="flex h-6 w-6 items-center justify-center rounded-full bg-red-500 text-white text-xs font-bold">
            {items.length}
          </span>
          <h2 className="font-semibold text-red-900">Needs Attention</h2>
        </div>
      </div>
      
      {/* Items */}
      <ul className="divide-y divide-grey-100">
        {items.map((item) => {
          const config = typeConfig[item.type];
          return (
            <li 
              key={item.id}
              className={cn("px-4 py-3 flex items-center justify-between gap-3", config.bgClass)}
            >
              <div className="flex items-center gap-3 min-w-0">
                <span className="text-xl">{config.icon}</span>
                <div className="min-w-0">
                  <p className="font-medium text-grey-900 truncate">{item.title}</p>
                  <p className="text-sm text-grey-500 truncate">{item.subtitle}</p>
                </div>
              </div>
              <button 
                onClick={item.action.onClick}
                className={cn(
                  "shrink-0 h-9 px-4 text-sm font-medium rounded-lg transition-colors",
                  actionVariants[item.action.variant]
                )}
              >
                {item.action.label}
              </button>
            </li>
          );
        })}
      </ul>
    </section>
  );
}
```

## 5. Stat Cards

```tsx
// src/components/dashboard/StatCard.tsx

interface StatCardProps {
  icon: string;
  value: string | number;
  label: string;
  trend?: 'up' | 'down' | 'stable';
}

export function StatCard({ icon, value, label, trend }: StatCardProps) {
  return (
    <div className="bg-white rounded-xl border border-grey-200 p-4 text-center">
      <span className="text-2xl">{icon}</span>
      <p className="mt-1 text-2xl font-bold text-grey-900 tabular-nums flex items-center justify-center gap-1">
        {value}
        {trend === 'up' && <span className="text-green-500 text-sm">▲</span>}
        {trend === 'down' && <span className="text-red-500 text-sm">▼</span>}
      </p>
      <p className="text-xs text-grey-500 mt-1">{label}</p>
    </div>
  );
}

// Usage
<section>
  <h2 className="text-sm font-medium text-grey-500 mb-3">TODAY</h2>
  <div className="grid grid-cols-3 gap-3">
    <StatCard icon="📞" value={12} label="Calls handled" trend="up" />
    <StatCard icon="💷" value="£2,340" label="Coming in" />
    <StatCard icon="⭐" value={2} label="New reviews" trend="up" />
  </div>
</section>
```

## 6. Cash Health Bar

```tsx
// src/components/dashboard/CashHealthBar.tsx

interface CashHealthProps {
  collected: number;
  billed: number;
  overdue: number;
  overdueCount: number;
}

export function CashHealthBar({ collected, billed, overdue, overdueCount }: CashHealthProps) {
  const percentage = billed > 0 ? Math.round((collected / billed) * 100) : 100;
  
  // Determine status
  let status: 'healthy' | 'warning' | 'critical';
  if (percentage >= 80) status = 'healthy';
  else if (percentage >= 60) status = 'warning';
  else status = 'critical';
  
  const statusStyles = {
    healthy: {
      bg: 'bg-green-50',
      border: 'border-green-200',
      bar: 'bg-green-500',
      text: 'text-green-700',
    },
    warning: {
      bg: 'bg-amber-50',
      border: 'border-amber-200',
      bar: 'bg-amber-500',
      text: 'text-amber-700',
    },
    critical: {
      bg: 'bg-red-50',
      border: 'border-red-200',
      bar: 'bg-red-500',
      text: 'text-red-700',
    },
  };
  
  const styles = statusStyles[status];

  return (
    <section className={cn("rounded-xl border p-4", styles.bg, styles.border)}>
      <div className="flex items-center justify-between mb-3">
        <h2 className="font-semibold text-grey-900">Cash Health</h2>
        <span className="text-sm text-grey-500">This month</span>
      </div>
      
      {/* Progress Bar */}
      <div className="h-3 bg-grey-200 rounded-full overflow-hidden mb-2">
        <div 
          className={cn("h-full transition-all duration-500", styles.bar)}
          style={{ width: `${Math.min(percentage, 100)}%` }}
        />
      </div>
      
      {/* Stats */}
      <div className="flex items-center justify-between text-sm">
        <span className="text-grey-600">
          <strong className="text-grey-900">£{collected.toLocaleString()}</strong>
          {' '}collected of £{billed.toLocaleString()} billed
        </span>
        <span className={cn("font-medium", styles.text)}>{percentage}%</span>
      </div>
      
      {/* Overdue Warning */}
      {overdue > 0 && (
        <div className="mt-3 flex items-center justify-between text-amber-700">
          <span className="text-sm">
            ⚠️ {overdueCount} invoice{overdueCount > 1 ? 's' : ''} overdue (£{overdue.toLocaleString()})
          </span>
          <button className="text-sm font-medium underline">View all</button>
        </div>
      )}
      
      {/* Success Message */}
      {status === 'healthy' && overdue === 0 && (
        <div className="mt-3 p-3 bg-white rounded-lg">
          <p className="text-sm text-grey-600">✨ Excellent collection rate this month!</p>
        </div>
      )}
    </section>
  );
}
```

## 7. Customer Snapshot

```tsx
// src/components/dashboard/CustomerSnapshot.tsx

interface CustomerSnapshotProps {
  total: number;
  repeatRate: number;
  ltv: number;
  ltvCacRatio: number;
}

export function CustomerSnapshot({ total, repeatRate, ltv, ltvCacRatio }: CustomerSnapshotProps) {
  const ratioHealth = ltvCacRatio >= 5 ? 'good' : ltvCacRatio >= 3 ? 'ok' : 'bad';
  
  return (
    <section className="bg-white rounded-xl border border-grey-200 p-4">
      <div className="flex items-center justify-between mb-3">
        <h2 className="font-semibold text-grey-900">Your customers</h2>
        <Link href="/dashboard/customers" className="text-sm text-brand-primary font-medium">
          View all →
        </Link>
      </div>
      
      <div className="grid grid-cols-4 gap-2 text-center">
        <div className="bg-grey-100 rounded-lg p-2">
          <p className="text-lg font-bold text-grey-900">{total}</p>
          <p className="text-xs text-grey-500">total</p>
        </div>
        <div className="bg-grey-100 rounded-lg p-2">
          <p className="text-lg font-bold text-grey-900">{repeatRate}%</p>
          <p className="text-xs text-grey-500">repeat</p>
        </div>
        <div className="bg-grey-100 rounded-lg p-2">
          <p className="text-lg font-bold text-grey-900">£{ltv}</p>
          <p className="text-xs text-grey-500">LTV</p>
        </div>
        <div className={cn(
          "rounded-lg p-2",
          ratioHealth === 'good' ? "bg-green-100" : ratioHealth === 'ok' ? "bg-amber-100" : "bg-red-100"
        )}>
          <p className={cn(
            "text-lg font-bold",
            ratioHealth === 'good' ? "text-green-700" : ratioHealth === 'ok' ? "text-amber-700" : "text-red-700"
          )}>
            {ltvCacRatio}:1
          </p>
          <p className={cn(
            "text-xs",
            ratioHealth === 'good' ? "text-green-600" : ratioHealth === 'ok' ? "text-amber-600" : "text-red-600"
          )}>
            ratio
          </p>
        </div>
      </div>
      
      {/* Insight */}
      <div className="mt-3 p-3 bg-grey-50 rounded-lg">
        <p className="text-sm text-grey-600">
          💡 {ltvCacRatio >= 10 
            ? `Excellent economics. Each £1 on marketing returns £${ltvCacRatio} in customer value.`
            : ltvCacRatio >= 5
              ? 'Strong customer economics. Keep it up!'
              : 'Focus on improving customer retention to boost LTV.'
          }
        </p>
      </div>
    </section>
  );
}
```

## 8. List Item

```tsx
// src/components/ui/ListItem.tsx

interface ListItemProps {
  title: string;
  subtitle: string;
  meta?: string;
  badge?: {
    label: string;
    variant: 'default' | 'primary' | 'success' | 'warning' | 'danger';
  };
  action?: {
    label: string;
    variant: 'primary' | 'secondary' | 'warning';
    onClick: () => void;
  };
  highlighted?: boolean;
}

const badgeVariants = {
  default: 'bg-grey-100 text-grey-600',
  primary: 'bg-blue-100 text-blue-700',
  success: 'bg-green-100 text-green-700',
  warning: 'bg-amber-100 text-amber-700',
  danger: 'bg-red-100 text-red-700',
};

const actionVariants = {
  primary: 'bg-brand-primary hover:bg-brand-primary-hover text-white',
  secondary: 'bg-grey-100 hover:bg-grey-200 text-grey-600',
  warning: 'bg-amber-500 hover:bg-amber-600 text-white',
};

export function ListItem({ title, subtitle, meta, badge, action, highlighted }: ListItemProps) {
  return (
    <li className={cn(
      "px-4 py-4 flex items-center justify-between gap-3",
      highlighted && "bg-red-50/50"
    )}>
      <div className="min-w-0">
        <div className="flex items-center gap-2">
          <p className="font-medium text-grey-900">{title}</p>
          {badge && (
            <span className={cn(
              "px-2 py-0.5 text-xs font-medium rounded-full",
              badgeVariants[badge.variant]
            )}>
              {badge.label}
            </span>
          )}
        </div>
        <p className="text-sm text-grey-500 mt-0.5">{subtitle}</p>
        {meta && (
          <p className={cn(
            "text-xs mt-1",
            highlighted ? "text-red-600" : "text-grey-500"
          )}>
            {meta}
          </p>
        )}
      </div>
      {action && (
        <button 
          onClick={action.onClick}
          className={cn(
            "shrink-0 h-9 px-4 text-sm font-medium rounded-lg transition-colors",
            actionVariants[action.variant]
          )}
        >
          {action.label}
        </button>
      )}
    </li>
  );
}
```

## 9. Summary Cards (Invoice page header)

```tsx
// src/components/ui/SummaryCards.tsx

interface SummaryCard {
  value: string;
  label: string;
  variant: 'default' | 'danger' | 'success';
}

const variants = {
  default: 'bg-white border-grey-200 text-grey-900',
  danger: 'bg-red-50 border-red-200 text-red-600',
  success: 'bg-green-50 border-green-200 text-green-600',
};

export function SummaryCards({ cards }: { cards: SummaryCard[] }) {
  return (
    <div className="px-4 py-4 grid grid-cols-3 gap-3">
      {cards.map((card, i) => (
        <div 
          key={i}
          className={cn(
            "rounded-xl border p-3 text-center",
            variants[card.variant]
          )}
        >
          <p className="text-xl font-bold tabular-nums">{card.value}</p>
          <p className="text-xs">{card.label}</p>
        </div>
      ))}
    </div>
  );
}

// Usage
<SummaryCards cards={[
  { value: '£2,340', label: 'Outstanding', variant: 'default' },
  { value: '£780', label: 'Overdue', variant: 'danger' },
  { value: '£4,200', label: 'Collected', variant: 'success' },
]} />
```

## 10. Filter Tabs

```tsx
// src/components/ui/FilterTabs.tsx

interface FilterTab {
  id: string;
  label: string;
  count?: number;
}

export function FilterTabs({ 
  tabs, 
  activeTab, 
  onChange 
}: { 
  tabs: FilterTab[];
  activeTab: string;
  onChange: (id: string) => void;
}) {
  return (
    <div className="px-4 pb-3 flex gap-2 overflow-x-auto">
      {tabs.map((tab) => (
        <button
          key={tab.id}
          onClick={() => onChange(tab.id)}
          className={cn(
            "px-4 py-2 text-sm font-medium rounded-full whitespace-nowrap transition-colors",
            activeTab === tab.id
              ? "bg-brand-primary text-white"
              : "bg-grey-100 text-grey-600 hover:bg-grey-200"
          )}
        >
          {tab.label}
          {tab.count !== undefined && ` (${tab.count})`}
        </button>
      ))}
    </div>
  );
}
```

## 11. Form Elements

```tsx
// src/components/ui/Input.tsx

interface InputProps extends React.InputHTMLAttributes<HTMLInputElement> {
  label?: string;
  error?: string;
  hint?: string;
}

export function Input({ label, error, hint, className, ...props }: InputProps) {
  return (
    <div className="space-y-1.5">
      {label && (
        <label className="text-sm font-medium text-grey-700">{label}</label>
      )}
      <input
        className={cn(
          "w-full h-11 px-4 bg-white border rounded-lg text-grey-900",
          "placeholder:text-grey-400",
          "focus:outline-none focus:ring-2 focus:ring-brand-primary focus:border-transparent",
          "transition-shadow",
          error ? "border-red-500" : "border-grey-300",
          className
        )}
        {...props}
      />
      {hint && !error && (
        <p className="text-xs text-grey-500">{hint}</p>
      )}
      {error && (
        <p className="text-sm text-red-600">{error}</p>
      )}
    </div>
  );
}

// src/components/ui/Select.tsx

interface SelectProps extends React.SelectHTMLAttributes<HTMLSelectElement> {
  label?: string;
  options: { value: string; label: string }[];
}

export function Select({ label, options, className, ...props }: SelectProps) {
  return (
    <div className="space-y-1.5">
      {label && (
        <label className="text-sm font-medium text-grey-700">{label}</label>
      )}
      <select
        className={cn(
          "w-full h-11 px-4 bg-white border border-grey-300 rounded-lg text-grey-900",
          "focus:outline-none focus:ring-2 focus:ring-brand-primary",
          className
        )}
        {...props}
      >
        {options.map((opt) => (
          <option key={opt.value} value={opt.value}>{opt.label}</option>
        ))}
      </select>
    </div>
  );
}

// src/components/ui/Toggle.tsx

interface ToggleProps {
  label: string;
  description?: string;
  checked: boolean;
  onChange: (checked: boolean) => void;
}

export function Toggle({ label, description, checked, onChange }: ToggleProps) {
  return (
    <label className="flex items-center justify-between p-4 bg-blue-50 rounded-xl cursor-pointer">
      <div>
        <p className="font-medium text-grey-900">{label}</p>
        {description && (
          <p className="text-sm text-grey-500">{description}</p>
        )}
      </div>
      <div className="relative">
        <input 
          type="checkbox" 
          className="sr-only peer" 
          checked={checked}
          onChange={(e) => onChange(e.target.checked)}
        />
        <div className="w-11 h-6 bg-grey-200 rounded-full peer peer-checked:bg-brand-primary transition-colors" />
        <div className="absolute left-0.5 top-0.5 w-5 h-5 bg-white rounded-full shadow peer-checked:translate-x-5 transition-transform" />
      </div>
    </label>
  );
}
```

## 12. Buttons

```tsx
// src/components/ui/Button.tsx

interface ButtonProps extends React.ButtonHTMLAttributes<HTMLButtonElement> {
  variant?: 'primary' | 'secondary' | 'danger' | 'ghost';
  size?: 'sm' | 'md' | 'lg';
  icon?: React.ReactNode;
  loading?: boolean;
}

const variants = {
  primary: 'bg-brand-primary hover:bg-brand-primary-hover text-white',
  secondary: 'bg-white hover:bg-grey-50 text-grey-700 border border-grey-300',
  danger: 'bg-red-600 hover:bg-red-700 text-white',
  ghost: 'bg-transparent hover:bg-grey-100 text-grey-600',
};

const sizes = {
  sm: 'h-9 px-4 text-sm',
  md: 'h-11 px-6 text-base',
  lg: 'h-12 px-8 text-lg',
};

export function Button({ 
  variant = 'primary', 
  size = 'md', 
  icon,
  loading,
  children,
  className,
  disabled,
  ...props 
}: ButtonProps) {
  return (
    <button
      className={cn(
        "font-medium rounded-lg transition-colors flex items-center justify-center gap-2",
        variants[variant],
        sizes[size],
        (disabled || loading) && "opacity-50 cursor-not-allowed",
        className
      )}
      disabled={disabled || loading}
      {...props}
    >
      {loading ? (
        <svg className="animate-spin h-5 w-5" viewBox="0 0 24 24">
          <circle className="opacity-25" cx="12" cy="12" r="10" stroke="currentColor" strokeWidth="4" fill="none" />
          <path className="opacity-75" fill="currentColor" d="M4 12a8 8 0 018-8V0C5.373 0 0 5.373 0 12h4z" />
        </svg>
      ) : icon}
      {children}
    </button>
  );
}

// Icon button variant
export function IconButton({ 
  icon, 
  onClick, 
  className 
}: { 
  icon: React.ReactNode;
  onClick?: () => void;
  className?: string;
}) {
  return (
    <button 
      onClick={onClick}
      className={cn(
        "w-10 h-10 flex items-center justify-center text-grey-400 hover:text-grey-600 hover:bg-grey-100 rounded-lg transition-colors",
        className
      )}
    >
      {icon}
    </button>
  );
}
```

## 13. Fixed Bottom Button

```tsx
// src/components/ui/FixedBottomButton.tsx

interface FixedBottomButtonProps {
  children: React.ReactNode;
  onClick?: () => void;
  loading?: boolean;
  disabled?: boolean;
  icon?: React.ReactNode;
}

export function FixedBottomButton({ children, onClick, loading, disabled, icon }: FixedBottomButtonProps) {
  return (
    <div className="fixed bottom-0 left-0 right-0 max-w-md mx-auto bg-white border-t border-grey-200 px-4 py-4 safe-area-pb">
      <Button 
        className="w-full" 
        size="lg"
        onClick={onClick}
        loading={loading}
        disabled={disabled}
        icon={icon}
      >
        {children}
      </Button>
    </div>
  );
}
```

## 14. Celebration Modal

```tsx
// src/components/ui/CelebrationModal.tsx

interface CelebrationModalProps {
  isOpen: boolean;
  onClose: () => void;
  title: string;
  subtitle: string;
  amount: string;
  emoji?: string;
}

export function CelebrationModal({ 
  isOpen, 
  onClose, 
  title, 
  subtitle, 
  amount,
  emoji = '🎉'
}: CelebrationModalProps) {
  if (!isOpen) return null;
  
  return (
    <div className="fixed inset-0 bg-black/50 flex items-center justify-center z-50">
      <div className="bg-white rounded-2xl p-8 text-center max-w-sm mx-4 shadow-2xl">
        <span className="text-6xl">{emoji}</span>
        <h2 className="mt-4 text-2xl font-bold text-grey-900">{title}</h2>
        <p className="mt-2 text-grey-600">{subtitle}</p>
        <p className="mt-4 text-4xl font-bold text-green-600">{amount}</p>
        <Button className="mt-6 w-full" onClick={onClose}>
          Nice!
        </Button>
      </div>
    </div>
  );
}

// Usage
<CelebrationModal
  isOpen={showCelebration}
  onClose={() => setShowCelebration(false)}
  title="Payment received!"
  subtitle="Mrs. Patterson paid her invoice"
  amount="+£285"
/>
```

## 15. Toast Notifications

```tsx
// src/components/ui/Toast.tsx

interface ToastProps {
  message: string;
  variant?: 'success' | 'error' | 'info';
  isVisible: boolean;
}

const variants = {
  success: { bg: 'bg-grey-900', icon: '✓', iconColor: 'text-green-400' },
  error: { bg: 'bg-red-600', icon: '✕', iconColor: 'text-white' },
  info: { bg: 'bg-grey-900', icon: 'ℹ', iconColor: 'text-blue-400' },
};

export function Toast({ message, variant = 'success', isVisible }: ToastProps) {
  if (!isVisible) return null;
  
  const config = variants[variant];
  
  return (
    <div className="fixed bottom-24 left-4 right-4 mx-auto max-w-sm z-50">
      <div className={cn(
        "px-4 py-3 rounded-lg shadow-lg flex items-center gap-3 text-white",
        config.bg
      )}>
        <span className={config.iconColor}>{config.icon}</span>
        <span>{message}</span>
      </div>
    </div>
  );
}
```

## 16. Empty States

```tsx
// src/components/ui/EmptyState.tsx

interface EmptyStateProps {
  icon: string;
  title: string;
  description: string;
  action?: {
    label: string;
    onClick: () => void;
  };
}

export function EmptyState({ icon, title, description, action }: EmptyStateProps) {
  return (
    <div className="text-center py-12 px-4">
      <div className="w-16 h-16 bg-blue-100 rounded-full flex items-center justify-center mx-auto text-3xl">
        {icon}
      </div>
      <h3 className="mt-4 text-lg font-semibold text-grey-900">{title}</h3>
      <p className="mt-2 text-grey-500 max-w-sm mx-auto">{description}</p>
      {action && (
        <Button className="mt-6" onClick={action.onClick}>
          {action.label}
        </Button>
      )}
    </div>
  );
}

// Usage
<EmptyState
  icon="📄"
  title="No invoices yet"
  description="Create your first invoice in 60 seconds."
  action={{ label: 'Create invoice', onClick: () => router.push('/dashboard/invoices/new') }}
/>
```

---

# PAGE TEMPLATES

## Dashboard Page

```tsx
// src/app/(dashboard)/page.tsx

export default function DashboardPage() {
  return (
    <>
      <Header greeting title="Dave" />
      <main className="px-4 py-6 space-y-6 pb-24">
        <NeedsAttentionFeed items={attentionItems} />
        
        <section>
          <h2 className="text-sm font-medium text-grey-500 mb-3">TODAY</h2>
          <div className="grid grid-cols-3 gap-3">
            <StatCard icon="📞" value={12} label="Calls handled" trend="up" />
            <StatCard icon="💷" value="£2,340" label="Coming in" />
            <StatCard icon="⭐" value={2} label="New reviews" trend="up" />
          </div>
        </section>
        
        <CashHealthBar collected={4200} billed={5800} overdue={780} overdueCount={3} />
        
        <CustomerSnapshot total={142} repeatRate={34} ltv={656} ltvCacRatio={17} />
      </main>
    </>
  );
}
```

## Invoice List Page

```tsx
// src/app/(dashboard)/invoices/page.tsx

export default function InvoicesPage() {
  const [activeFilter, setActiveFilter] = useState('all');
  
  return (
    <>
      <Header 
        title="Invoices" 
        action={
          <Button size="sm" icon={<PlusIcon className="w-4 h-4" />}>
            New
          </Button>
        }
      />
      <main className="pb-24">
        <SummaryCards cards={[
          { value: '£2,340', label: 'Outstanding', variant: 'default' },
          { value: '£780', label: 'Overdue', variant: 'danger' },
          { value: '£4,200', label: 'Collected', variant: 'success' },
        ]} />
        
        <FilterTabs
          tabs={[
            { id: 'all', label: 'All' },
            { id: 'draft', label: 'Draft' },
            { id: 'sent', label: 'Sent' },
            { id: 'overdue', label: 'Overdue' },
            { id: 'paid', label: 'Paid' },
          ]}
          activeTab={activeFilter}
          onChange={setActiveFilter}
        />
        
        <ul className="divide-y divide-grey-100">
          {invoices.map(invoice => (
            <ListItem
              key={invoice.id}
              title={invoice.number}
              subtitle={`${invoice.customerName} • £${invoice.total}`}
              meta={invoice.statusText}
              badge={{ label: invoice.status, variant: invoice.statusVariant }}
              action={invoice.action}
              highlighted={invoice.status === 'overdue'}
            />
          ))}
        </ul>
      </main>
    </>
  );
}
```

## New Invoice Page

```tsx
// src/app/(dashboard)/invoices/new/page.tsx

export default function NewInvoicePage() {
  return (
    <>
      <Header backButton title="New Invoice" onBack={() => router.back()} />
      <main className="px-4 py-6 space-y-6 pb-32">
        <Input 
          label="Customer"
          placeholder="Search or add customer..."
          value={customer}
          onChange={(e) => setCustomer(e.target.value)}
          hint="07700 900123 • 14 Oak Road, SE15 4AA"
        />
        
        <div className="space-y-3">
          <label className="text-sm font-medium text-grey-700">Items</label>
          <div className="bg-grey-50 rounded-xl p-4 space-y-3">
            {lineItems.map((item, i) => (
              <div key={i} className="flex gap-3">
                <Input 
                  placeholder="Description"
                  value={item.description}
                  className="flex-1"
                />
                <Input 
                  placeholder="£"
                  value={item.amount}
                  className="w-24 text-right tabular-nums"
                />
              </div>
            ))}
          </div>
          <button className="text-sm text-brand-primary font-medium flex items-center gap-1">
            <PlusIcon className="w-4 h-4" />
            Add item
          </button>
        </div>
        
        <div className="bg-grey-50 rounded-xl p-4 space-y-2">
          <div className="flex justify-between text-sm">
            <span className="text-grey-600">Subtotal</span>
            <span className="text-grey-900 tabular-nums">£165.00</span>
          </div>
          <div className="flex justify-between text-sm">
            <span className="text-grey-600">VAT (20%)</span>
            <span className="text-grey-900 tabular-nums">£33.00</span>
          </div>
          <div className="flex justify-between text-lg font-semibold border-t border-grey-200 pt-2 mt-2">
            <span className="text-grey-900">Total</span>
            <span className="text-grey-900 tabular-nums">£198.00</span>
          </div>
        </div>
        
        <Select 
          label="Due date"
          options={[
            { value: '14', label: '14 days (11 Dec 2025)' },
            { value: '7', label: '7 days (4 Dec 2025)' },
            { value: '30', label: '30 days (27 Dec 2025)' },
          ]}
        />
        
        <Toggle
          label="Send immediately"
          description="Email invoice to customer now"
          checked={sendNow}
          onChange={setSendNow}
        />
      </main>
      
      <FixedBottomButton 
        icon={<SendIcon className="w-5 h-5" />}
        onClick={handleSend}
        loading={isSending}
      >
        Send Invoice — £198.00
      </FixedBottomButton>
    </>
  );
}
```

---

# CLAUDE CODE PROMPT

```
Build all UI components for Covered AI using the patterns in /specs/11-UI-COMPONENT-REFERENCE.md

Create these files:

1. Update tailwind.config.js with the color palette
2. Update globals.css with Inter font and utility classes

3. Create components:
   - src/components/layout/DashboardLayout.tsx
   - src/components/layout/Header.tsx
   - src/components/layout/BottomNavigation.tsx
   - src/components/dashboard/NeedsAttentionFeed.tsx
   - src/components/dashboard/StatCard.tsx
   - src/components/dashboard/CashHealthBar.tsx
   - src/components/dashboard/CustomerSnapshot.tsx
   - src/components/ui/Button.tsx
   - src/components/ui/Input.tsx
   - src/components/ui/Select.tsx
   - src/components/ui/Toggle.tsx
   - src/components/ui/ListItem.tsx
   - src/components/ui/SummaryCards.tsx
   - src/components/ui/FilterTabs.tsx
   - src/components/ui/FixedBottomButton.tsx
   - src/components/ui/CelebrationModal.tsx
   - src/components/ui/Toast.tsx
   - src/components/ui/EmptyState.tsx

4. Create pages:
   - src/app/(dashboard)/page.tsx
   - src/app/(dashboard)/invoices/page.tsx
   - src/app/(dashboard)/invoices/new/page.tsx

Use the exact Tailwind classes from the spec. Mobile-first. Match the visual mockup at /dashboard-mockup.html exactly.
```
