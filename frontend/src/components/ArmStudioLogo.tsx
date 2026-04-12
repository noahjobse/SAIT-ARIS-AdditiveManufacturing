interface ArmStudioLogoProps {
  size?: number;
  className?: string;
}

export default function ArmStudioLogo({ size = 56, className }: ArmStudioLogoProps) {
  return (
    <svg
      width={size}
      height={size}
      viewBox="0 0 56 56"
      fill="none"
      xmlns="http://www.w3.org/2000/svg"
      className={className}
    >
      <defs>
        <linearGradient id="armLogoGrad" x1="0%" y1="0%" x2="100%" y2="100%">
          <stop offset="0%" stopColor="#f97316" />
          <stop offset="100%" stopColor="#9333ea" />
        </linearGradient>
      </defs>
      {/* Outer hex border */}
      <polygon
        points="28,2 52,15 52,41 28,54 4,41 4,15"
        fill="none"
        stroke="url(#armLogoGrad)"
        strokeWidth="1.5"
        opacity="0.5"
      />
      {/* Inner hex fill */}
      <polygon
        points="28,8 46,18 46,38 28,48 10,38 10,18"
        fill="rgba(249,115,22,0.06)"
      />
      {/* Robotic arm: base → elbow → wrist → tip */}
      <path
        d="M22 42 L22 28 L30 20 L42 16"
        stroke="url(#armLogoGrad)"
        strokeWidth="2.5"
        strokeLinecap="round"
        strokeLinejoin="round"
      />
      {/* Joints */}
      <circle cx="22" cy="28" r="2.5" fill="#f97316" />
      <circle cx="30" cy="20" r="2.5" fill="#c084fc" />
      <circle cx="42" cy="16" r="2.5" fill="#9333ea" />
      {/* Base mount */}
      <rect x="18" y="42" width="8" height="3" rx="1.5" fill="#f97316" opacity="0.7" />
    </svg>
  );
}
