import React, { useState } from 'react';
import { Calendar, ChevronLeft, ChevronRight, Filter, Maximize2, Minimize2 } from 'lucide-react';
import { NewsSource } from '../types';
import { DayPicker } from 'react-day-picker';
import 'react-day-picker/dist/style.css';
import { Popover } from '@headlessui/react';

interface ControlsProps {
  sources: NewsSource[];
  activeSourceIds: string[];
  onSourceToggle: (sourceId: string) => void;
  onToggleAll: (active: boolean) => void;
  onDateChange: (date: Date) => void;
  selectedDate: Date;
}

const Controls: React.FC<ControlsProps> = ({
  sources,
  activeSourceIds,
  onSourceToggle,
  onToggleAll,
  onDateChange,
  selectedDate,
}) => {
  const [isFilterOpen, setIsFilterOpen] = useState(false);
  const [isCalendarOpen, setIsCalendarOpen] = useState(false);
  
  const handlePreviousDay = () => {
    const newDate = new Date(selectedDate);
    newDate.setDate(newDate.getDate() - 1);
    onDateChange(newDate);
  };
  
  const handleNextDay = () => {
    const newDate = new Date(selectedDate);
    newDate.setDate(newDate.getDate() + 1);
    onDateChange(newDate);
  };
  
  const formatDate = (date: Date) => {
    return date.toLocaleDateString('en-US', {
      weekday: 'short',
      month: 'short',
      day: 'numeric',
      year: 'numeric',
    });
  };
  
  const areAllActive = activeSourceIds.length === sources.length;
  
  return (
    <div className="bg-white rounded-lg shadow-md p-4 mb-6">
      <div className="flex flex-col sm:flex-row justify-between items-center">
        {/* Date navigation */}
        <div className="flex items-center space-x-2 mb-4 sm:mb-0">
          <button 
            onClick={handlePreviousDay}
            className="p-2 rounded-full hover:bg-gray-100"
          >
            <ChevronLeft size={20} />
          </button>
          
          <Popover className="relative">
            <Popover.Button as="div" className="flex items-center px-3 py-2 bg-gray-100 rounded-md cursor-pointer select-none" onClick={() => setIsCalendarOpen(!isCalendarOpen)}>
              <Calendar size={18} className="mr-2 text-blue-600" />
              <span className="font-medium">{formatDate(selectedDate)}</span>
            </Popover.Button>
            <Popover.Panel className="absolute z-20 mt-2 left-1/2 -translate-x-1/2 bg-white rounded-lg shadow-lg p-2 border border-gray-200">
              <DayPicker
                mode="single"
                selected={selectedDate}
                onSelect={(date) => {
                  if (date) {
                    onDateChange(date);
                    setIsCalendarOpen(false);
                  }
                }}
                defaultMonth={selectedDate}
              />
            </Popover.Panel>
          </Popover>
          
          <button 
            onClick={handleNextDay}
            className="p-2 rounded-full hover:bg-gray-100"
          >
            <ChevronRight size={20} />
          </button>
        </div>
        
        {/* Source filters */}
        <div className="flex items-center">
          <button 
            onClick={() => setIsFilterOpen(!isFilterOpen)}
            className="flex items-center px-3 py-2 bg-gray-100 rounded-md hover:bg-gray-200 mr-3"
          >
            <Filter size={18} className="mr-2 text-blue-600" />
            <span>Filter Sources</span>
          </button>
          
          <button 
            onClick={() => onToggleAll(!areAllActive)}
            className="flex items-center px-3 py-2 bg-blue-100 rounded-md hover:bg-blue-200"
          >
            {areAllActive ? (
              <>
                <Minimize2 size={18} className="mr-2 text-blue-600" />
                <span>Hide All</span>
              </>
            ) : (
              <>
                <Maximize2 size={18} className="mr-2 text-blue-600" />
                <span>Show All</span>
              </>
            )}
          </button>
        </div>
      </div>
      
      {/* Expandable filter list */}
      {isFilterOpen && (
        <div className="mt-4 pt-4 border-t grid grid-cols-2 sm:grid-cols-3 md:grid-cols-5 gap-3">
          {sources.map((source) => {
            const isActive = activeSourceIds.includes(source.short_id);
            return (
              <div 
                key={source.short_id} 
                className={`flex items-center p-2 rounded-md cursor-pointer ${
                  isActive ? 'bg-blue-50 border border-blue-200' : 'bg-gray-50 border border-gray-200'
                }`}
                onClick={() => onSourceToggle(source.short_id)}
              >
                <div 
                  className="w-4 h-4 rounded-full mr-2"
                  style={{ backgroundColor: source.color }}
                ></div>
                <span className="text-sm">{source.name}</span>
              </div>
            );
          })}
        </div>
      )}
    </div>
  );
};

export default Controls;