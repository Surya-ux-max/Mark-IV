import React from 'react';
import { CloudSun, Wind, Droplets, Gauge, Compass } from 'lucide-react';

export const WeatherWorkspace = ({ aiResponse, isTyping, onSubmitQuery }) => {
  return (
    <div className="w-full h-full p-8 max-w-6xl mx-auto space-y-8 select-text font-sans text-white">
      
      {/* Workspace Header */}
      <div className="border-b border-[#1E1E1E] pb-4 flex justify-between items-end">
        <div>
          <span className="hud-font text-[9px] text-[#9A9A9A] uppercase tracking-[0.25em]">SPECIALIZED AGENT WORKSPACE</span>
          <h1 className="hud-font text-4xl font-extrabold uppercase tracking-wider text-white mt-1">WEATHER</h1>
        </div>
        <div className="hud-font text-xs text-[#9A9A9A] uppercase tracking-widest text-right">
          <span>LATITUDE: 13.0827° N</span><br />
          <span>LONGITUDE: 80.2707° E</span>
        </div>
      </div>

      {/* Assistant Voice/Text Output Container */}
      <div className="p-6 border border-[#1E1E1E] bg-[#0A0A0A] space-y-3">
        <div className="flex justify-between items-center text-[9px] hud-font text-[#9A9A9A] uppercase tracking-widest">
          <span>WEATHER AGENT VOICE & TEXT OUTPUT</span>
          <span>LIVE METEOROLOGICAL FEED</span>
        </div>
        {isTyping ? (
          <p className="hud-font text-sm text-slate-400 animate-pulse uppercase tracking-widest">
            Querying satellite radar & weather APIs...
          </p>
        ) : (
          <p className="text-xl md:text-2xl font-semibold leading-relaxed text-white">
            {aiResponse || "Tomorrow will be cloudy with a maximum temperature of 31°C. Light evening breeze expected."}
          </p>
        )}
      </div>

      {/* Current Weather Overview & Metrics */}
      <div className="grid grid-cols-1 md:grid-cols-3 gap-6">
        
        {/* Main Temperature Card */}
        <div className="p-6 border border-[#1E1E1E] bg-[#0A0A0A] flex flex-col justify-between space-y-6">
          <div className="flex justify-between items-start">
            <div>
              <p className="hud-font text-xs text-[#9A9A9A] uppercase tracking-widest">CURRENT LOCATION</p>
              <h2 className="text-2xl font-bold text-white mt-1 uppercase">LOCAL REGION</h2>
            </div>
            <CloudSun className="w-8 h-8 text-white stroke-[1.5]" />
          </div>
          <div>
            <div className="text-6xl font-extrabold tracking-tighter text-white">29°C</div>
            <p className="hud-font text-xs text-[#9A9A9A] uppercase tracking-widest mt-2">Partly Cloudy · Feels like 32°C</p>
          </div>
        </div>

        {/* Detailed Metrics */}
        <div className="p-6 border border-[#1E1E1E] bg-[#0A0A0A] grid grid-cols-2 gap-4">
          <div className="border border-[#1E1E1E] p-3 flex flex-col justify-between">
            <div className="flex items-center space-x-2 text-[#9A9A9A] text-xs hud-font uppercase">
              <Droplets className="w-3.5 h-3.5 text-white" />
              <span>Humidity</span>
            </div>
            <p className="text-2xl font-bold text-white">68%</p>
          </div>

          <div className="border border-[#1E1E1E] p-3 flex flex-col justify-between">
            <div className="flex items-center space-x-2 text-[#9A9A9A] text-xs hud-font uppercase">
              <Wind className="w-3.5 h-3.5 text-white" />
              <span>Wind Speed</span>
            </div>
            <p className="text-2xl font-bold text-white">14 km/h</p>
          </div>

          <div className="border border-[#1E1E1E] p-3 flex flex-col justify-between">
            <div className="flex items-center space-x-2 text-[#9A9A9A] text-xs hud-font uppercase">
              <Gauge className="w-3.5 h-3.5 text-white" />
              <span>AQI Index</span>
            </div>
            <p className="text-2xl font-bold text-white">42 (Good)</p>
          </div>

          <div className="border border-[#1E1E1E] p-3 flex flex-col justify-between">
            <div className="flex items-center space-x-2 text-[#9A9A9A] text-xs hud-font uppercase">
              <Compass className="w-3.5 h-3.5 text-white" />
              <span>Pressure</span>
            </div>
            <p className="text-2xl font-bold text-white">1013 hPa</p>
          </div>
        </div>

        {/* Rain Probability & Air Status */}
        <div className="p-6 border border-[#1E1E1E] bg-[#0A0A0A] flex flex-col justify-between space-y-4">
          <p className="hud-font text-xs text-[#9A9A9A] uppercase tracking-widest">PRECIPITATION PROBABILITY</p>
          <div className="space-y-2">
            <div className="flex justify-between text-xs hud-font">
              <span>CHANCE OF RAIN</span>
              <span className="font-bold">20%</span>
            </div>
            <div className="w-full bg-[#1E1E1E] h-2">
              <div className="bg-white h-full w-[20%]" />
            </div>
          </div>
          <p className="hud-font text-[10px] text-[#9A9A9A] uppercase leading-relaxed">
            Satellite radar indicates low storm likelihood for the next 24 hours.
          </p>
        </div>

      </div>

      {/* 5-Day Forecast Cards */}
      <div className="space-y-3">
        <h3 className="hud-font text-xs text-[#9A9A9A] uppercase tracking-widest">5-DAY METEOROLOGICAL FORECAST</h3>
        <div className="grid grid-cols-2 md:grid-cols-5 gap-3">
          {[
            { day: 'TODAY', temp: '29° / 24°', status: 'PARTLY CLOUDY' },
            { day: 'TOMORROW', temp: '31° / 25°', status: 'OVERCAST' },
            { day: 'WEDNESDAY', temp: '30° / 24°', status: 'LIGHT SHOWERS' },
            { day: 'THURSDAY', temp: '32° / 26°', status: 'CLEAR SKY' },
            { day: 'FRIDAY', temp: '33° / 26°', status: 'SUNNY' },
          ].map((item, idx) => (
            <div key={idx} className="p-4 border border-[#1E1E1E] bg-[#0A0A0A] space-y-2">
              <p className="hud-font text-[10px] text-[#9A9A9A] uppercase tracking-widest">{item.day}</p>
              <p className="text-lg font-bold text-white">{item.temp}</p>
              <p className="hud-font text-[9px] text-[#9A9A9A] uppercase">{item.status}</p>
            </div>
          ))}
        </div>
      </div>

      {/* Suggested Weather Queries */}
      <div className="p-6 border border-[#1E1E1E] bg-[#0A0A0A] space-y-3">
        <h4 className="hud-font text-xs text-[#9A9A9A] uppercase tracking-widest">SUGGESTED QUERIES</h4>
        <div className="flex flex-wrap gap-2">
          {["What is the weather in London?", "Will it rain this evening?", "What is the humidity level?", "Show weekend forecast"].map((q, i) => (
            <button
              key={i}
              onClick={() => onSubmitQuery(q)}
              className="px-3 py-1.5 border border-[#1E1E1E] hover:border-white text-xs hud-font uppercase text-[#9A9A9A] hover:text-white transition-all cursor-pointer"
            >
              {q}
            </button>
          ))}
        </div>
      </div>

    </div>
  );
};

export default WeatherWorkspace;
