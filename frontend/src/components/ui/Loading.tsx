import React from "react";
import { cn } from "../../utils";

interface LoadingSpinnerProps {
  size?: "sm" | "md" | "lg";
  className?: string;
}

const LoadingSpinner: React.FC<LoadingSpinnerProps> = ({
  size = "md",
  className,
}) => {
  const sizeClasses = {
    sm: "w-4 h-4",
    md: "w-6 h-6",
    lg: "w-8 h-8",
  };

  return (
    <div
      className={cn(
        "animate-spin rounded-full border-2 border-gray-300 border-t-blue-600",
        sizeClasses[size],
        className
      )}
    />
  );
};

interface LoadingProps {
  message?: string;
  size?: "sm" | "md" | "lg";
  className?: string;
}

const Loading: React.FC<LoadingProps> = ({
  message = "Loading...",
  size = "md",
  className,
}) => {
  return (
    <div
      className={cn("flex flex-col items-center justify-center p-8", className)}
    >
      <LoadingSpinner size={size} />
      {message && <p className="mt-2 text-sm text-gray-600">{message}</p>}
    </div>
  );
};

export { LoadingSpinner, Loading };
