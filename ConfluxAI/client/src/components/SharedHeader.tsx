import React from 'react';
import { motion } from 'framer-motion';
import { Switch } from '@/components/ui/switch';
import { Badge } from '@/components/ui/badge';
import { Settings } from 'lucide-react';
import { toast } from '@/hooks/use-toast';

interface SharedHeaderProps {
  title: string;
  subtitle: string;
  icon: React.ReactNode;
  isProduction: boolean;
  onProductionToggle: (checked: boolean) => void;
  testId?: string;
}

const SharedHeader: React.FC<SharedHeaderProps> = ({
  title,
  subtitle,
  icon,
  isProduction,
  onProductionToggle,
  testId = 'webhook-mode-toggle'
}) => {
  return (
    <motion.header 
      initial={{ opacity: 0, y: -10 }}
      animate={{ opacity: 1, y: 0 }}
      transition={{ duration: 0.3, ease: "easeOut" }}
      className="glass sticky top-0 z-10 p-4 shadow-lg border-b border-white/10"
      role="banner"
    >
      <div className="flex items-center justify-between">
        <div className="flex items-center gap-3">
          <motion.div 
            initial={{ scale: 0.8 }}
            animate={{ scale: 1 }}
            transition={{ duration: 0.2, delay: 0.1 }}
            className="flex-shrink-0"
          >
            {icon}
          </motion.div>
          
          <motion.div 
            initial={{ opacity: 0, x: -10 }}
            animate={{ opacity: 1, x: 0 }}
            transition={{ duration: 0.3, delay: 0.15 }}
          >
            <h1 className="text-xl font-semibold text-foreground">{title}</h1>
            <p className="text-sm text-muted-foreground">{subtitle}</p>
          </motion.div>
        </div>
        
        {/* Webhook Mode Toggle */}
        <motion.div 
          initial={{ opacity: 0, x: 10 }}
          animate={{ opacity: 1, x: 0 }}
          transition={{ duration: 0.3, delay: 0.2 }}
          className="flex items-center gap-3" 
          data-testid={testId}
        >
          <div className="flex items-center gap-2">
            <Settings 
              className="w-4 h-4 text-muted-foreground" 
              aria-hidden="true"
            />
            <fieldset className="flex items-center gap-2">
              <legend className="sr-only">Webhook Mode Selection</legend>
              
              <label 
                htmlFor="test-mode" 
                className={`text-sm font-medium transition-colors cursor-pointer ${
                  !isProduction 
                    ? 'text-orange-600 dark:text-orange-400' 
                    : 'text-muted-foreground hover:text-foreground'
                }`}
              >
                Test
              </label>
              
              <Switch
                id="webhook-mode-switch"
                checked={isProduction}
                onCheckedChange={(checked) => {
                  onProductionToggle(checked);
                  toast({
                    title: checked ? "Production Mode" : "Test Mode",
                    description: checked ? "Using production webhook" : "Using test webhook",
                  });
                }}
                aria-label={`Switch to ${isProduction ? 'test' : 'production'} mode`}
                data-testid={`${testId.split('-')[0]}-production-mode-switch`}
              />
              
              <label 
                htmlFor="production-mode" 
                className={`text-sm font-medium transition-colors cursor-pointer ${
                  isProduction 
                    ? 'text-green-600 dark:text-green-400' 
                    : 'text-muted-foreground hover:text-foreground'
                }`}
              >
                Production
              </label>
            </fieldset>
          </div>
        </motion.div>
      </div>
      
      {/* Mode Indicator */}
      <motion.div 
        initial={{ opacity: 0, y: 5 }}
        animate={{ opacity: 1, y: 0 }}
        transition={{ duration: 0.3, delay: 0.25 }}
        className="mt-3"
      >
        <Badge 
          variant={isProduction ? "default" : "secondary"}
          className={`inline-flex items-center gap-2 transition-all duration-200 ${
            isProduction 
              ? 'bg-green-100 dark:bg-green-900/30 text-green-800 dark:text-green-300 border-green-200 dark:border-green-700 hover:bg-green-200 dark:hover:bg-green-900/50' 
              : 'bg-orange-100 dark:bg-orange-900/30 text-orange-800 dark:text-orange-300 border-orange-200 dark:border-orange-700 hover:bg-orange-200 dark:hover:bg-orange-900/50'
          }`}
        >
          <motion.div 
            animate={{ opacity: [1, 0.5, 1] }}
            transition={{ duration: 2, repeat: Infinity, ease: "easeInOut" }}
            className={`w-2 h-2 rounded-full ${
              isProduction ? 'bg-green-500' : 'bg-orange-500'
            }`}
          />
          <span>
            {isProduction ? 'Production Mode Active' : 'Test Mode Active'}
          </span>
        </Badge>
      </motion.div>
    </motion.header>
  );
};

export default SharedHeader;