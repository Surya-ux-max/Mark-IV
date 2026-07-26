import React, { useState } from 'react';
import { Mail, Send, Inbox, FileText, CheckCircle } from 'lucide-react';

export const EmailWorkspace = ({ aiResponse, isTyping, onSubmitQuery }) => {
  const [recipient, setRecipient] = useState('suryapr.exe14@gmail.com');
  const [subject, setSubject] = useState('');
  const [body, setBody] = useState('');

  const handleSend = (e) => {
    e.preventDefault();
    if (recipient && subject) {
      onSubmitQuery(`Send email to ${recipient} with subject "${subject}" and body "${body}"`);
    }
  };

  return (
    <div className="w-full h-full p-8 max-w-6xl mx-auto space-y-8 select-text font-sans text-white">
      
      {/* Header */}
      <div className="border-b border-[#1E1E1E] pb-4 flex justify-between items-end">
        <div>
          <span className="hud-font text-[9px] text-[#9A9A9A] uppercase tracking-[0.25em]">SPECIALIZED AGENT WORKSPACE</span>
          <h1 className="hud-font text-4xl font-extrabold uppercase tracking-wider text-white mt-1">EMAIL</h1>
        </div>
        <div className="hud-font text-xs text-[#9A9A9A] uppercase tracking-widest text-right">
          <span>SMTP CLIENT: PYTHON smtplib</span><br />
          <span>ACCOUNT: suryapr.exe14@gmail.com</span>
        </div>
      </div>

      {/* Voice + Text Output Box */}
      <div className="p-6 border border-[#1E1E1E] bg-[#0A0A0A] space-y-3">
        <div className="flex justify-between items-center text-[9px] hud-font text-[#9A9A9A] uppercase tracking-widest">
          <span>EMAIL AGENT SUMMARY</span>
          <span>SMTP GATEWAY</span>
        </div>
        {isTyping ? (
          <p className="hud-font text-sm text-slate-400 animate-pulse uppercase tracking-widest">
            Connecting to SMTP server & compiling email draft...
          </p>
        ) : (
          <p className="text-xl md:text-2xl font-semibold leading-relaxed text-white">
            {aiResponse || "Email agent active. System address set to suryapr.exe14@gmail.com. Ready to compose or read messages."}
          </p>
        )}
      </div>

      {/* Main Grid: Inbox & Compose Form */}
      <div className="grid grid-cols-1 md:grid-cols-3 gap-6">
        
        {/* Inbox / Recent Messages (1 col) */}
        <div className="p-6 border border-[#1E1E1E] bg-[#0A0A0A] space-y-4">
          <h3 className="hud-font text-xs text-[#9A9A9A] uppercase tracking-widest">RECENT MESSAGES</h3>
          <div className="space-y-3">
            {[
              { sender: 'SurveX System', subj: 'Daily OS Health Summary', time: '09:00 AM' },
              { sender: 'GitHub Notifications', subj: 'Pull Request #4 Approved', time: 'Yesterday' },
              { sender: 'Calendar Agent', subj: 'Reminder: System Eng Class', time: 'Yesterday' },
            ].map((msg, idx) => (
              <div key={idx} className="p-3 border border-[#1E1E1E] bg-black hover:border-white/40 transition-all space-y-1">
                <div className="flex justify-between text-[10px] hud-font text-[#9A9A9A] uppercase">
                  <span>{msg.sender}</span>
                  <span>{msg.time}</span>
                </div>
                <p className="text-xs font-bold text-white uppercase">{msg.subj}</p>
              </div>
            ))}
          </div>
        </div>

        {/* Compose Email Form (2 cols) */}
        <div className="md:col-span-2 p-6 border border-[#1E1E1E] bg-[#0A0A0A] space-y-4">
          <h3 className="hud-font text-xs text-white font-bold uppercase tracking-widest">COMPOSE EMAIL VIA AI AGENT</h3>
          <form onSubmit={handleSend} className="space-y-4">
            <div className="space-y-1">
              <label className="hud-font text-[10px] text-[#9A9A9A] uppercase">RECIPIENT EMAIL</label>
              <input
                type="email"
                value={recipient}
                onChange={e => setRecipient(e.target.value)}
                placeholder="suryapr.exe14@gmail.com"
                className="w-full bg-black border border-[#1E1E1E] px-4 py-2.5 text-xs text-white placeholder-[#9A9A9A] focus:outline-none focus:border-white hud-font"
              />
            </div>

            <div className="space-y-1">
              <label className="hud-font text-[10px] text-[#9A9A9A] uppercase">SUBJECT</label>
              <input
                type="text"
                value={subject}
                onChange={e => setSubject(e.target.value)}
                placeholder="Enter subject line..."
                className="w-full bg-black border border-[#1E1E1E] px-4 py-2.5 text-xs text-white placeholder-[#9A9A9A] focus:outline-none focus:border-white hud-font"
              />
            </div>

            <div className="space-y-1">
              <label className="hud-font text-[10px] text-[#9A9A9A] uppercase">MESSAGE BODY</label>
              <textarea
                value={body}
                onChange={e => setBody(e.target.value)}
                placeholder="Write your email body or ask SurveX to generate it..."
                rows={5}
                className="w-full bg-black border border-[#1E1E1E] px-4 py-2.5 text-xs text-white placeholder-[#9A9A9A] focus:outline-none focus:border-white hud-font leading-relaxed resize-none"
              />
            </div>

            <button
              type="submit"
              className="px-6 py-3 bg-white text-black font-bold hud-font text-xs uppercase tracking-wider cursor-pointer hover:bg-slate-200 flex items-center space-x-2"
            >
              <Send className="w-3.5 h-3.5" />
              <span>Send Email via Agent</span>
            </button>
          </form>
        </div>

      </div>

    </div>
  );
};

export default EmailWorkspace;
