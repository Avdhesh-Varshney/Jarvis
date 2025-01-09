import React, { useState } from 'react';
import {
  Divide,
  Minus,
  Plus,
  X,
  RotateCcw,
  Equal,
  Percent,
  Square,
  Calculator,
  History,
  Delete,
  Copy
} from 'lucide-react';

interface HistoryItem {
  calculation: string;
  result: string;
  timestamp: Date;
}

function App() {
  const [display, setDisplay] = useState('0');
  const [previousValue, setPreviousValue] = useState<number | null>(null);
  const [operation, setOperation] = useState<string | null>(null);
  const [newNumber, setNewNumber] = useState(true);
  const [history, setHistory] = useState<HistoryItem[]>([]);
  const [showHistory, setShowHistory] = useState(false);
  const [expression, setExpression] = useState('');

  const scientificFunctions = {
    sin: Math.sin,
    cos: Math.cos,
    tan: Math.tan,
    log: Math.log10,
    ln: Math.log,
    sqrt: Math.sqrt,
    square: (n: number) => n * n,
  };

  const handleNumber = (num: string) => {
    if (newNumber) {
      setDisplay(num);
      setExpression(expression + num);
      setNewNumber(false);
    } else {
      setDisplay(display === '0' ? num : display + num);
      setExpression(expression + num);
    }
  };

  const handleDecimal = () => {
    if (newNumber) {
      setDisplay('0.');
      setExpression(expression + '0.');
      setNewNumber(false);
    } else if (!display.includes('.')) {
      setDisplay(display + '.');
      setExpression(expression + '.');
    }
  };

  const handleOperator = (op: string) => {
    const current = parseFloat(display);
    if (previousValue === null) {
      setPreviousValue(current);
      setExpression(display + ' ' + op + ' ');
    } else if (operation) {
      const result = calculate(previousValue, current, operation);
      setPreviousValue(result);
      setDisplay(String(result));
      setExpression(String(result) + ' ' + op + ' ');
    }
    setOperation(op);
    setNewNumber(true);
  };

  const handleScientific = (func: keyof typeof scientificFunctions) => {
    const current = parseFloat(display);
    const result = scientificFunctions[func](current);
    setDisplay(String(result));
    setExpression(`${func}(${current}) = ${result}`);
    setNewNumber(true);
    
    addToHistory(`${func}(${current})`, String(result));
  };

  const calculate = (prev: number, current: number, op: string): number => {
    switch (op) {
      case '+': return prev + current;
      case '-': return prev - current;
      case '×': return prev * current;
      case '÷': return prev / current;
      case '%': return (prev * current) / 100;
      default: return current;
    }
  };

  const handleEquals = () => {
    if (previousValue === null || operation === null) return;
    const current = parseFloat(display);
    const result = calculate(previousValue, current, operation);
    const fullExpression = `${expression}${display}`;
    
    setDisplay(String(result));
    addToHistory(fullExpression, String(result));
    setPreviousValue(null);
    setOperation(null);
    setNewNumber(true);
    setExpression('');
  };

  const addToHistory = (calculation: string, result: string) => {
    setHistory(prev => [{
      calculation,
      result,
      timestamp: new Date()
    }, ...prev.slice(0, 9)]);
  };

  const clear = () => {
    setDisplay('0');
    setPreviousValue(null);
    setOperation(null);
    setNewNumber(true);
    setExpression('');
  };

  const clearHistory = () => {
    setHistory([]);
  };

  const copyToClipboard = (text: string) => {
    navigator.clipboard.writeText(text);
  };

  const Button = ({ children, onClick, className = '' }: any) => (
    <button
      onClick={onClick}
      className={`p-3 rounded-lg transition-colors ${className} hover:bg-opacity-90`}
    >
      {children}
    </button>
  );

  return (
    <div className="min-h-screen bg-gradient-to-br from-gray-800 to-gray-900 flex items-center justify-center p-4">
      <div className="bg-gray-100 p-6 rounded-2xl shadow-2xl w-full max-w-4xl flex gap-6">
        {/* Calculator Section */}
        <div className="flex-1">
          <div className="flex items-center justify-between mb-6">
            <h1 className="text-2xl font-bold text-gray-800 flex items-center gap-2">
              <Calculator className="w-6 h-6" />
              Scientific Calculator
            </h1>
            <button 
              onClick={() => setShowHistory(!showHistory)}
              className="p-2 rounded-lg bg-gray-200 hover:bg-gray-300 transition-colors"
            >
              <History className="w-5 h-5" />
            </button>
          </div>
          
          <div className="bg-white p-4 rounded-xl mb-4 shadow-inner">
            <div className="text-gray-600 text-right mb-1 min-h-[1.5rem] text-sm">
              {expression || '\u00A0'}
            </div>
            <div className="text-right text-4xl font-medium text-gray-800 break-all">
              {display}
            </div>
          </div>

          <div className="grid grid-cols-4 gap-2">
            {/* Scientific Functions */}
            <Button onClick={() => handleScientific('sin')} className="bg-indigo-200 text-indigo-800">
              sin
            </Button>
            <Button onClick={() => handleScientific('cos')} className="bg-indigo-200 text-indigo-800">
              cos
            </Button>
            <Button onClick={() => handleScientific('tan')} className="bg-indigo-200 text-indigo-800">
              tan
            </Button>
            <Button onClick={() => handleScientific('log')} className="bg-indigo-200 text-indigo-800">
              log
            </Button>
            
            <Button onClick={() => handleScientific('ln')} className="bg-indigo-200 text-indigo-800">
              ln
            </Button>
            <Button onClick={() => handleScientific('sqrt')} className="bg-indigo-200 text-indigo-800">
              √
            </Button>
            <Button onClick={() => handleScientific('square')} className="bg-indigo-200 text-indigo-800">
              <Square className="w-5 h-5 mx-auto" />
            </Button>
            <Button onClick={() => handleOperator('%')} className="bg-indigo-200 text-indigo-800">
              <Percent className="w-5 h-5 mx-auto" />
            </Button>

            {/* Numbers and Basic Operations */}
            <Button onClick={clear} className="bg-red-200 text-red-800">
              <RotateCcw className="w-5 h-5 mx-auto" />
            </Button>
            <Button onClick={() => handleOperator('÷')} className="bg-amber-200 text-amber-800">
              <Divide className="w-5 h-5 mx-auto" />
            </Button>
            <Button onClick={() => handleOperator('×')} className="bg-amber-200 text-amber-800">
              <X className="w-5 h-5 mx-auto" />
            </Button>
            <Button onClick={() => handleOperator('-')} className="bg-amber-200 text-amber-800">
              <Minus className="w-5 h-5 mx-auto" />
            </Button>

            <Button onClick={() => handleNumber('7')} className="bg-gray-200">7</Button>
            <Button onClick={() => handleNumber('8')} className="bg-gray-200">8</Button>
            <Button onClick={() => handleNumber('9')} className="bg-gray-200">9</Button>
            <Button onClick={() => handleOperator('+')} className="bg-amber-200 text-amber-800 row-span-2">
              <Plus className="w-5 h-5 mx-auto" />
            </Button>

            <Button onClick={() => handleNumber('4')} className="bg-gray-200">4</Button>
            <Button onClick={() => handleNumber('5')} className="bg-gray-200">5</Button>
            <Button onClick={() => handleNumber('6')} className="bg-gray-200">6</Button>

            <Button onClick={() => handleNumber('1')} className="bg-gray-200">1</Button>
            <Button onClick={() => handleNumber('2')} className="bg-gray-200">2</Button>
            <Button onClick={() => handleNumber('3')} className="bg-gray-200">3</Button>
            <Button onClick={handleEquals} className="bg-green-500 text-white row-span-2">
              <Equal className="w-5 h-5 mx-auto" />
            </Button>

            <Button onClick={() => handleNumber('0')} className="bg-gray-200 col-span-2">0</Button>
            <Button onClick={handleDecimal} className="bg-gray-200">.</Button>
          </div>
        </div>

        {/* History Section */}
        <div className={`w-80 bg-white rounded-xl p-4 shadow-inner transition-all transform ${showHistory ? 'translate-x-0 opacity-100' : 'translate-x-full opacity-0'}`}>
          <div className="flex items-center justify-between mb-4">
            <h2 className="text-lg font-semibold text-gray-800">History</h2>
            <button 
              onClick={clearHistory}
              className="p-2 rounded-lg text-red-600 hover:bg-red-50 transition-colors"
              title="Clear History"
            >
              <Delete className="w-4 h-4" />
            </button>
          </div>
          
          <div className="space-y-3">
            {history.map((item, index) => (
              <div key={index} className="p-3 bg-gray-50 rounded-lg">
                <div className="flex items-center justify-between">
                  <span className="text-sm text-gray-500">
                    {item.timestamp.toLocaleTimeString()}
                  </span>
                  <button
                    onClick={() => copyToClipboard(item.result)}
                    className="p-1 hover:bg-gray-200 rounded transition-colors"
                    title="Copy result"
                  >
                    <Copy className="w-4 h-4" />
                  </button>
                </div>
                <div className="text-gray-600">{item.calculation}</div>
                <div className="text-lg font-medium text-gray-800">{item.result}</div>
              </div>
            ))}
            
            {history.length === 0 && (
              <div className="text-center text-gray-500 py-4">
                No calculations yet
              </div>
            )}
          </div>
        </div>
      </div>
    </div>
  );
}

export default App;