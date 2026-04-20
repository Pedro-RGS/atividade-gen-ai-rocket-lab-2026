import type { InputHTMLAttributes } from "react";

interface CustomInputProps extends InputHTMLAttributes<HTMLInputElement>{
  label?: string;
  error?: string;
}

export const CustomInput = ({
  label,
  error,
  className = '',
  id,
  ...props
}: CustomInputProps) => {
  const containerStyles = 'flex flex-col gap-1.5 w-full';

  const inputBaseStyles = `
  w-full px-4 py-2 bg-zinc-900 border rounded-none outline-none transition-all
  placeholder:text-zinc-500 text-white
  focus:border-yellow-500
  ${error ? "border-red-500" : "border-zinc-800"}
  ${className}`;

  return (
    <div className={containerStyles}>
      {label && (
        <label htmlFor={id} className="text-sm font-medium text-gray-700">
          {label}
        </label>
      )}

      <div className="relative">
        <input id={id} className={inputBaseStyles} {...props} />

        {error && (
          <span className="text-xs text-red-500 mt-1">{error}</span>
        )}
      </div>
    </div>
  );
}