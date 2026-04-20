import type { LucideIcon } from 'lucide-react';

interface CustomIconProps {
  icon: LucideIcon;
  size?: 'sm' | 'md' | 'lg';
  color?: 'primary' | 'secondary' | 'danger';
  className?: string;
}

export const CustomIcon = ({
  icon: IconComponent,
  size = 'md',
  color = 'primary',
  className = '',
}: CustomIconProps) => { 

  const sizes = {
    sm: 'w-4 h-4',
    md: 'w-6 h-6',
    lg: 'w-8 h-8',
  };

  const colors = {
    primary: "text-(--color-primary)",
    secondary: "text-gray-600",
    danger: "text-red-600",
  };

  const iconClasses = `${sizes[size]} ${colors[color]} ${className}`;

  return <IconComponent className={iconClasses} />;
}