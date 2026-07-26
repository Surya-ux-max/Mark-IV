import React, { useState } from 'react';
import { Calendar as CalendarIcon, Clock, CheckSquare, Plus } from 'lucide-react';

export const CalendarWorkspace = ({ aiResponse, isTyping, onSubmitQuery }) => {
  const [newEventTitle, setNewEventTitle] = useState('');
  const [newEventTime, setNewEventTime] = useState('');

  const daysInMonth = Array.from({ length: 31 }, (_, i) => i + 1);

  return (
    <div className="w-full h-full p-8 max-w-6xl mx-auto space-y-8 select-text font-sans text-white">
      
      {/* Header */}
      <div className="border-b border-[#1E1E1E] pb-4 flex justify-between items-end">
        <div>
          <span className="hud-font text-[9px] text-[#9A9A9A] uppercase tracking-[0.25em]">SPECIALIZED AGENT WORKSPACE</span>
          <h1 className="hud-font text-4xl font-extrabold uppercase tracking-wider text-white mt-1">CALENDAR</h1>
        </div>
        <div className="hud-font text-xs text-[#9A9A9A] uppercase tracking-widest text-right">
          <span>SCHEDULE DATABASE: POSTGRESQL / SQLITE</span><br />
          <span>TIMEZONE: LOCAL HOST</span>
        </div>
      </div>

      {/* Voice + Text Output Box */}
      <div className="p-6 border border-[#1E1E1E] bg-[#0A0A0A] space-y-3">
        <div className="flex justify-between items-center text-[9px] hud-font text-[#9A9A9A] uppercase tracking-widest">
          <span>CALENDAR AGENT VOICE SUMMARY</span>
          <span>SCHEDULE SCHEDULER</span>
        </div>
        {isTyping ? (
          <p className="hud-font text-sm text-slate-400 animate-pulse uppercase tracking-widest">
            Updating database calendar events & reminders...
          </p>
        ) : (
          <p className="text-xl md:text-2xl font-semibold leading-relaxed text-white">
            {aiResponse || "You have class at 10:00 AM. I will remind you 15 minutes before. Total 3 events scheduled for today."}
          </p>
        )}
      </div>

      {/* Main Grid: Calendar Grid & Agenda */}
      <div className="grid grid-cols-1 md:grid-cols-3 gap-6">
        
        {/* Month Calendar Grid (2 cols) */}
        <div className="md:col-span-2 p-6 border border-[#1E1E1E] bg-[#0A0A0A] space-y-4">
          <div className="flex justify-between items-center">
            <h3 className="hud-font text-xs text-white font-bold uppercase tracking-widest">JULY 2026</h3>
            <span className="hud-font text-[10px] text-[#9A9A9A] uppercase">31 DAYS</span>
          </div>

          <div className="grid grid-cols-7 gap-2 text-center hud-font text-xs">
            {['SUN', 'MON', 'TUE', 'WED', 'THU', 'FRI', 'SAT'].map(d => (
              <div key={d} className="py-2 text-[#9A9A9A] font-bold text-[10px]">{d}</div>
            ))}
            {daysInMonth.map(d => {
              const isToday = d === 26;
              const hasEvent = [10, 15, 26, 28].includes(d);
              return (
                <div
                  key={d}
                  className={`py-3 border flex flex-col items-center justify-between transition-all ${
                    isToday
                      ? 'border-white bg-white text-black font-extrabold'
                      : hasEvent
                      ? 'border-white/30 bg-white/5 text-white'
                      : 'border-[#1E1E1E] bg-black text-[#9A9A9A]'
                  }`}
                >
                  <span className="text-sm">{d}</span>
                  {hasEvent && !isToday && <div className="w-1.5 h-1.5 rounded-full bg-white mt-1" />}
                </div>
              );
            })}
          </div>
        </div>

        {/* Agenda & Tasks Column (1 col) */}
        <div className="space-y-6">
          
          {/* Today's Agenda */}
          <div className="p-6 border border-[#1E1E1E] bg-[#0A0A0A] space-y-4">
            <h3 className="hud-font text-xs text-[#9A9A9A] uppercase tracking-widest">TODAY'S AGENDA</h3>
            <div className="space-y-3">
              {[
                { time: '10:00 AM', title: 'System Engineering Class', duration: '1h' },
                { time: '02:30 PM', title: 'Supervisor LangGraph Review', duration: '45m' },
                { time: '06:00 PM', title: 'SurveX Release Build Check', duration: '30m' },
              ].map((ev, i) => (
                <div key={i} className="p-3 border border-[#1E1E1E] bg-black flex justify-between items-center">
                  <div>
                    <p className="text-xs font-bold text-white uppercase">{ev.title}</p>
                    <p className="hud-font text-[9px] text-[#9A9A9A] uppercase mt-0.5">{ev.time} · {ev.duration}</p>
                  </div>
                  <Clock className="w-3.5 h-3.5 text-[#9A9A9A]" />
                </div>
              ))}
            </div>
          </div>

          {/* Quick Schedule Input */}
          <div className="p-6 border border-[#1E1E1E] bg-[#0A0A0A] space-y-3">
            <h3 className="hud-font text-xs text-[#9A9A9A] uppercase tracking-widest">QUICK SCHEDULE REMINDER</h3>
            <form onSubmit={(e) => {
              e.preventDefault();
              if (newEventTitle.trim()) {
                onSubmitQuery(`Schedule ${newEventTitle} at ${newEventTime || '10 AM'}`);
                setNewEventTitle('');
                setNewEventTime('');
              }
            }} className="space-y-2">
              <input
                type="text"
                value={newEventTitle}
                onChange={e => setNewEventTitle(e.target.value)}
                placeholder="Event title (e.g. Class at 10 AM)..."
                className="w-full bg-black border border-[#1E1E1E] px-3 py-2 text-xs text-white placeholder-[#9A9A9A] focus:outline-none focus:border-white hud-font"
              />
              <button
                type="submit"
                className="w-full py-2 bg-white text-black font-bold hud-font text-xs uppercase tracking-wider cursor-pointer hover:bg-slate-200"
              >
                Add Reminder
              </button>
            </form>
          </div>

        </div>

      </div>

    </div>
  );
};

export default CalendarWorkspace;
