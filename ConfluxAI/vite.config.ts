import { defineConfig } from "vite";
import react from "@vitejs/plugin-react";
import path from "path";

export default defineConfig({
  plugins: [
    react(),
  ],
  resolve: {
    alias: {
      "@": path.resolve(import.meta.dirname, "client", "src"),
      "@shared": path.resolve(import.meta.dirname, "shared"),
      "@assets": path.resolve(import.meta.dirname, "attached_assets"),
    },
  },
  root: path.resolve(import.meta.dirname, "client"),
  build: {
    outDir: path.resolve(import.meta.dirname, "dist/public"),
    emptyOutDir: true,
    rollupOptions: {
      output: {
        manualChunks: {
          // Vendor chunk for large dependencies
          vendor: ['react', 'react-dom'],
          // UI components chunk
          ui: ['@radix-ui/react-dialog', '@radix-ui/react-dropdown-menu', '@radix-ui/react-tooltip'],
          // Motion and animations
          animations: ['framer-motion'],
          // Upload components (lazy loaded)
          uploads: ['./client/src/components/PDFUpload.tsx', './client/src/components/VideoUpload.tsx'],
        },
      },
    },
    // Performance optimizations
    chunkSizeWarningLimit: 1000,
    minify: 'esbuild', // Use esbuild instead of terser for faster builds
  },
  // Development optimizations
  optimizeDeps: {
    include: ['react', 'react-dom', 'framer-motion'],
    exclude: ['@testing-library/react', '@testing-library/jest-dom'],
  },
  server: {
    hmr: {
      overlay: false, // Disable error overlay for better DX
    },
  },
});
