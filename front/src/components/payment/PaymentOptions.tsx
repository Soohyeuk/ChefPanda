import React from 'react';
import { Link } from 'react-router-dom';

const options = [
  {
    label: 'Interview Coder Free',
    sublabel: 'Try it and see',
    price: '$0',
    period: '/ month',
    features: [
      'Evaluate features',
      'Normal agent models',
    ],
    button: 'Get Started',
    link: '/subscribe/free',
    accent: false,
    badge: null,
    highlight: false,
    disabled: false,
  },
  {
    label: 'Interview Coder Pro',
    sublabel: 'Most popular',
    price: '$25',
    period: '/ month',
    features: [
      'Unlimited yearly usage',
      'Solving and debugging',
      'Most powerful agent models',
      '24/7 customer support',
    ],
    button: 'Subscribe',
    link: '/subscribe/annual',
    accent: true,
    badge: 'Most popular',
    highlight: true,
    subtext: '$300 billed annually',
    disabled: false,
  },
  {
    label: 'Interview Coder Pro',
    sublabel: 'Monthly subscription',
    price: '$60',
    period: '/ month',
    features: [
      'Unlimited monthly usage',
      'Solving and debugging',
      'Most powerful agent models',
      '24/7 customer support',
    ],
    button: 'Subscribe',
    link: 'https://buy.stripe.com/5kQ3cucKq6bv4JH3cp4gg00',
    accent: false,
    badge: null,
    highlight: false,
    disabled: false,
  },
];

function CheckIcon({ className = '' }) {
  return (
    <svg className={`w-5 h-5 inline-block mr-2 text-yellow-400 ${className}`} fill="none" stroke="currentColor" strokeWidth="2" viewBox="0 0 24 24">
      <path strokeLinecap="round" strokeLinejoin="round" d="M5 13l4 4L19 7" />
    </svg>
  );
}

function StarBadge() {
  return (
    <span className="absolute top-6 right-6 flex items-center gap-1 text-yellow-400 font-bold text-xs bg-yellow-900/20 px-3 py-1 rounded-full shadow-lg">
      <svg className="w-4 h-4 text-yellow-400" fill="none" stroke="currentColor" strokeWidth="2" viewBox="0 0 24 24">
        <path strokeLinecap="round" strokeLinejoin="round" d="M12 17.75L18.2 21l-1.64-7.03L22 9.24l-7.19-.61L12 2 9.19 8.63 2 9.24l5.44 4.73L5.8 21z" />
      </svg>
      Most popular
    </span>
  );
}

function CheckMark() {
  return (
    <svg className="w-6 h-6 text-yellow-400 absolute top-6 right-6" fill="none" stroke="currentColor" strokeWidth="2" viewBox="0 0 24 24">
      <path strokeLinecap="round" strokeLinejoin="round" d="M5 13l4 4L19 7" />
    </svg>
  );
}

export default function PaymentOptions() {
  const [selected, setSelected] = React.useState(1); // Default to most popular

  return (
    <div className="min-h-screen flex flex-col items-center justify-center bg-gradient-to-b from-black via-zinc-900 to-zinc-950 py-12 px-4">
      <h2 className="text-2xl md:text-4xl font-extrabold text-gray-100 mb-2 tracking-tight">Pricing</h2>
      <p className="text-base md:text-lg text-gray-400 mb-8 md:mb-12">Simple and transparent pricing for everyone.</p>
      <div className="flex flex-col md:flex-row gap-6 md:gap-8 w-full max-w-6xl justify-center items-stretch">
        {options.map((option, idx) => {
          const isSelected = selected === idx;
          return (
            <div
              key={option.label + idx}
              className={`flex-1 flex flex-col rounded-2xl border border-zinc-700 bg-zinc-900/80 shadow-xl px-6 py-8 md:px-8 md:py-10 transition-all duration-300 h-[28rem] min-w-0 w-full md:w-1/3 max-w-none
                ${isSelected ? 'ring-2 ring-yellow-400 ring-offset-2 ring-offset-zinc-950 z-10 shadow-yellow-400/30' : 'hover:scale-105 hover:shadow-2xl'}
              `}
              onClick={() => setSelected(idx)}
            >
              {option.badge && <StarBadge />}
              {isSelected && <CheckMark />}
              <div className="mb-2 text-base md:text-lg font-semibold text-gray-100">
                {option.label}
                {option.accent && <span className="ml-1 text-yellow-400 font-bold">Pro</span>}
                {!option.accent && idx === 0 && <span className="ml-1 text-yellow-400 font-bold">Free</span>}
              </div>
              <div className="mb-1 text-gray-400 text-xs md:text-sm">{option.sublabel}</div>
              <div className="flex items-end mb-2">
                <span className="text-3xl md:text-4xl font-extrabold text-gray-100">{option.price}</span>
                <span className="ml-2 text-gray-400 text-base md:text-lg">{option.period}</span>
              </div>
              {option.subtext && <div className="mb-2 text-gray-500 text-xs md:text-sm line-through">{option.subtext}</div>}
              <div className="border-b border-zinc-700 my-3 md:my-4" />
              <ul className="flex-1 mb-6 md:mb-8 space-y-2 md:space-y-3 text-left">
                {option.features.map((feature, i) => (
                  <li key={feature} className="text-gray-200 text-sm md:text-base flex items-center">
                    <CheckIcon />
                    {feature}
                  </li>
                ))}
              </ul>
              <Link
                to={option.link}
                className={`w-full py-2 md:py-3 rounded-lg font-bold text-base md:text-lg transition-all duration-200 flex items-center justify-center gap-2
                  ${isSelected ? 'bg-yellow-400 text-black shadow-yellow-400/40 shadow-lg' : 'bg-zinc-800 text-yellow-400 border border-yellow-400 hover:bg-yellow-400 hover:text-black'}
                `}
                tabIndex={0}
                aria-disabled={option.disabled}
                onClick={e => option.disabled && e.preventDefault()}
              >
                {option.button}
                <span className="ml-1">→</span>
              </Link>
            </div>
          );
        })}
      </div>
    </div>
  );
} 