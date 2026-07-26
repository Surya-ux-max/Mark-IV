import React, { useEffect, useState } from 'react';

/**
 * Supervisor Multi-Agent Intent Transition Overlay.
 * Displays the multi-agent delegation sequence step by step.
 */
export const IntentTransition = ({ targetAgents = [], onComplete }) => {
  const [step, setStep] = useState(0);

  const agentList = Array.isArray(targetAgents) ? targetAgents : [targetAgents];
  const formattedNames = agentList.map(a => (a || 'GENERAL').replace('_agent', '').replace('_cleaner', '').toUpperCase());
  const mainTarget = formattedNames[0] || 'GENERAL';
  const isMultiAgent = formattedNames.length > 1;

  useEffect(() => {
    const timer1 = setTimeout(() => setStep(1), 120);
    const timer2 = setTimeout(() => setStep(2), 280);
    const timer3 = setTimeout(() => setStep(3), 420);
    const timer4 = setTimeout(() => {
      if (onComplete) onComplete();
    }, 520);

    return () => {
      clearTimeout(timer1);
      clearTimeout(timer2);
      clearTimeout(timer3);
      clearTimeout(timer4);
    };
  }, [onComplete]);

  return (
    <div className="fixed inset-0 z-50 bg-black/90 backdrop-blur-md flex flex-col items-center justify-center font-sans animate-[fadeIn_0.15s_ease-out]">
      <div className="w-full max-w-md p-8 border border-white/10 bg-[#0A0A0A] rounded-none shadow-2xl flex flex-col items-center space-y-6">
        
        {/* Animated indicator */}
        <div className="relative w-12 h-12 flex items-center justify-center">
          <div className="absolute inset-0 border border-white/20 animate-spin" />
          <div className="w-3 h-3 bg-white" />
        </div>

        {/* Status text sequence */}
        <div className="text-center space-y-2">
          <p className="hud-font text-[10px] text-slate-500 uppercase tracking-[0.25em]">
            SUPERVISOR MULTI-AGENT ORCHESTRATOR
          </p>
          
          <h3 className="hud-font text-base md:text-lg font-bold text-white uppercase tracking-wider">
            {step === 0 && 'Analyzing Intent & Agent Dependencies...'}
            {step === 1 && (
              isMultiAgent 
                ? `Delegating: ${formattedNames.join(' → ')}` 
                : `Intent Detected: ${mainTarget}`
            )}
            {step === 2 && `Opening ${mainTarget} Workspace...`}
            {step >= 3 && 'Multi-Agent Operations Complete.'}
          </h3>
        </div>

        {/* Progress steps */}
        <div className="w-full space-y-1 pt-2">
          <div className="h-[2px] w-full bg-white/10 overflow-hidden">
            <div 
              className="h-full bg-white transition-all duration-150"
              style={{ width: `${(step + 1) * 25}%` }}
            />
          </div>
          <div className="flex justify-between text-[8px] hud-font text-slate-600 uppercase tracking-widest pt-1">
            <span>SUPERVISOR_ROUTING</span>
            <span>{isMultiAgent ? `${formattedNames.length}_AGENTS_SYNCED` : 'SINGLE_AGENT_SYNC'}</span>
            <span>100% NOMINAL</span>
          </div>
        </div>
      </div>
    </div>
  );
};

export default IntentTransition;
