/**
 * Centralized gradient definitions for ConfluxAI
 * These gradients provide consistent theming across the application
 */

export const TAB_GRADIENTS = {
  chat: 'from-blue-500 to-purple-600',
  pdf: 'from-green-500 to-blue-600',
  image: 'from-purple-500 to-pink-600',
  video: 'from-blue-500 to-cyan-600',
  audio: 'from-emerald-500 to-teal-600',
  documents: 'from-slate-500 to-gray-600'
} as const;

export const BUTTON_GRADIENTS = {
  primary: 'from-blue-500 to-purple-600',
  secondary: 'from-gray-500 to-slate-600',
  success: 'from-green-500 to-emerald-600',
  warning: 'from-yellow-500 to-orange-600',
  danger: 'from-red-500 to-pink-600',
  info: 'from-cyan-500 to-blue-600'
} as const;

export const BACKGROUND_GRADIENTS = {
  primary: 'from-blue-50 via-white to-purple-50 dark:from-slate-900 dark:via-slate-800 dark:to-purple-900/20',
  secondary: 'from-gray-50 via-white to-slate-50 dark:from-slate-900 dark:via-slate-800 dark:to-slate-900',
  warm: 'from-orange-50 via-white to-red-50 dark:from-slate-900 dark:via-slate-800 dark:to-red-900/20',
  cool: 'from-cyan-50 via-white to-blue-50 dark:from-slate-900 dark:via-slate-800 dark:to-blue-900/20'
} as const;

export const TEXT_GRADIENTS = {
  primary: 'from-blue-600 via-purple-600 to-blue-600',
  secondary: 'from-gray-600 via-slate-600 to-gray-600',
  warm: 'from-orange-600 via-red-600 to-pink-600',
  cool: 'from-cyan-600 via-blue-600 to-indigo-600'
} as const;

export type TabGradient = keyof typeof TAB_GRADIENTS;
export type ButtonGradient = keyof typeof BUTTON_GRADIENTS;
export type BackgroundGradient = keyof typeof BACKGROUND_GRADIENTS;
export type TextGradient = keyof typeof TEXT_GRADIENTS;
