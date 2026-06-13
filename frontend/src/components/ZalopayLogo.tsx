interface ZalopayLogoProps {
  size?: "sm" | "md" | "lg" | "xl";
  className?: string;
  dark?: boolean;
}

const sizeMap = {
  sm: "text-xl",
  md: "text-2xl",
  lg: "text-3xl",
  xl: "text-5xl",
};

export function ZalopayLogo({ size = "md", className = "", dark }: ZalopayLogoProps) {
  return (
    <span
      className={`font-black tracking-tight select-none ${sizeMap[size]} ${className}`}
      style={{ fontFamily: "'Inter', sans-serif", letterSpacing: "-0.03em" }}
    >
      <span style={{ color: dark ? "#FFFFFF" : "#0B47D9" }}>Zalo</span>
      <span style={{ color: dark ? "#7DFFA5" : "#06C755" }}>pay</span>
    </span>
  );
}
