import * as React from "react"
import { cva, type VariantProps } from "class-variance-authority"
import { motion, type MotionProps } from "framer-motion"

import { cn } from "@/lib/utils"
import { TEXT_GRADIENTS, type TextGradient } from "@/theme/gradients"

const gradientTextVariants = cva(
  "bg-clip-text text-transparent bg-gradient-to-r font-semibold",
  {
    variants: {
      gradient: {
        primary: `from-blue-600 via-purple-600 to-blue-600`,
        secondary: `from-gray-600 via-slate-600 to-gray-600`,
        warm: `from-orange-600 via-red-600 to-pink-600`,
        cool: `from-cyan-600 via-blue-600 to-indigo-600`,
      },
      size: {
        sm: "text-sm",
        default: "text-base",
        lg: "text-lg",
        xl: "text-xl",
        "2xl": "text-2xl",
        "3xl": "text-3xl",
      },
    },
    defaultVariants: {
      gradient: "primary",
      size: "default",
    },
  }
)

export interface GradientTextProps
  extends React.HTMLAttributes<HTMLSpanElement>,
    VariantProps<typeof gradientTextVariants> {
  as?: "span" | "h1" | "h2" | "h3" | "h4" | "h5" | "h6" | "p"
  motionProps?: MotionProps
  animate?: boolean
}

const GradientText = React.forwardRef<HTMLElement, GradientTextProps>(
  ({ 
    className, 
    gradient, 
    size, 
    as: Component = "span", 
    motionProps, 
    animate = false,
    children,
    ...props 
  }, ref) => {
    const MotionComponent = motion[Component as keyof typeof motion] as any

    const defaultMotionProps: MotionProps = {
      initial: { backgroundPosition: "0% 50%" },
      animate: animate ? {
        backgroundPosition: ["0% 50%", "100% 50%", "0% 50%"],
      } : {},
      transition: {
        duration: 3,
        ease: "linear",
        repeat: Infinity,
      },
      ...motionProps
    }

    if (animate) {
      return (
        <MotionComponent
          ref={ref}
          className={cn(
            gradientTextVariants({ gradient, size }),
            "bg-[length:200%_auto]",
            className
          )}
          {...defaultMotionProps}
          {...props}
        >
          {children}
        </MotionComponent>
      )
    }

    return React.createElement(
      Component,
      {
        ref,
        className: cn(gradientTextVariants({ gradient, size }), className),
        ...props
      },
      children
    )
  }
)
GradientText.displayName = "GradientText"

export { GradientText, gradientTextVariants }
