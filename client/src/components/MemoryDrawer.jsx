import React, { useRef, useEffect } from 'react';
import { X, History } from 'lucide-react';

export const MemoryDrawer = ({ isOpen, onClose, conversations = [] }) => {
  const scrollRef = useRef(null);

  useEffect(() => {
    if (isOpen && scrollRef.current) {
      scrollRef.current.scrollTop = scrollRef.current.scrollHeight;
    }
  }, [isOpen, conversations]);

  if (!isOpen) return null;

  return (
    <>
      <div 
        className="fixed inset-0 z-40 bg-black/40 backdrop-blur-[2px]"
        onClick={onClose}
      />
      <div className="fixed top-0 right-0 bottom-0 w-[340px] z-50 bg-[#0A0A0A] border-l border-[#1E1E1E] flex flex-col shadow-2xl animate-[slideInRight_0.25s_ease-out] font-sans">
        
        {/* Header */}
        <div className="p-5 border-b border-[#1E1E1E] flex justify-between items-center">
          <div className="flex items-center space-x-2">
            <History className="w-4 h-4 text-white" />
            <span className="hud-font font-bold text-xs uppercase tracking-widest text-white">
              SESSION MEMORY
            </span>
          </div>
          <button
            onClick={onClose}
            className="p-1 border border-[#1E1E1E] text-[#9A9A9A] hover:text-white hover:border-white transition-all cursor-pointer"
          >
            <X className="w-4 h-4" />
          </button>
        </div>

        {/* Message Log List */}
        <div ref={scrollRef} className="flex-1 overflow-y-auto p-4 space-y-4 scrollbar-thin">
          {conversations.length === 0 ? (
            <p className="hud-font text-xs text-[#9A9A9A] uppercase tracking-widest text-center mt-10">
              No session memory logs.
            </p>
          ) : (
            conversations.map((msg, idx) => (
              <div key={idx} className="p-3 border border-[#1E1E1E] bg-black space-y-1">
                <div className="flex justify-between items-center text-[9px] hud-font">
                  <span className={`px-1.5 py-0.5 font-bold uppercase ${
                    msg.sender === 'operator' ? 'bg-white/10 text-white' : 'bg-white text-black'
                  }`}>
                    {msg.sender === 'operator' ? 'SURYA' : 'SURVEX'}
                  </span>
                  <span className="text-[#9A9A9A]">
                    {new Date(msg.timestamp || Date.now()).toLocaleTimeString(undefined, { hour: '2-digit', minute: '2-digit' })}
                  </span>
                </div>
                <p className="text-xs text-white leading-relaxed">{msg.message}</p>
              </div>
            ))
          )}
        </div>

        {/* Footer */}
        <div className="p-4 border-t border-[#1E1E1E] text-center">
          <span className="hud-font text-[9px] text-[#9A9A9A] uppercase tracking-widest">
            {conversations.length} MESSAGES IN ACTIVE SESSION
          </span>
        </div>

      </div>
    </>
  );
};

export default MemoryDrawer;
