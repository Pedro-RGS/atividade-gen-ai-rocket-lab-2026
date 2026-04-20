interface CustomImageProps {
  src: string;
  alt: string;
  variant?: "default" | "circle";
  className?: string;
}

export const CustomImage = ({ src, alt, className = "" }: CustomImageProps) => {
  return (
    <div
      className={`w-full h-full flex items-center justify-center ${className}`}
    >
      <img
        src={src}
        alt={alt}
        className="max-w-full max-h-full object-contain"
        loading="lazy"
      />
    </div>
  );
};