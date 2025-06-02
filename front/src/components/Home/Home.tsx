import React from 'react'
import Header from '@/components/Header/Header'
import { Button } from '@/components/ui/button'

const Home: React.FC = () => {
  return (
    <div className="w-full h-fit">
      <Header />
      <div className="flex flex-col md:flex-row items-center justify-center max-w-6xl mx-auto px-4 py-12 gap-8 md:gap-16">
        {/* Left: Text */}
        <div className="flex-1 flex flex-col items-start justify-center gap-6 max-w-xl">
          <h1 className="text-xl md:text-7xl font-extrabold text-[#23281C] leading-tight">
            Learn to cook<br />
            with a <span className="text-[#7A8674]">Chef Panda</span><br />
            experience.
          </h1>
          <p className="text-[#7A8674] text-lg md:text-xl max-w-md">
            Luxury pet grooming tailored to pamper your furry companion with care, style, and comfort.
          </p>
          <Button className="bg-[#7A8674] text-white px-6 py-3 rounded-lg font-semibold shadow hover:bg-[#6a7863] transition text-base md:text-lg">Book Appointment</Button>
          <div className="flex items-center gap-2 mt-2">
            <div className="flex -space-x-2">
              <img src="https://randomuser.me/api/portraits/men/32.jpg" alt="pet1" className="w-8 h-8 rounded-full border-2 border-white" />
              <img src="https://randomuser.me/api/portraits/women/44.jpg" alt="pet2" className="w-8 h-8 rounded-full border-2 border-white" />
              <img src="https://randomuser.me/api/portraits/men/45.jpg" alt="pet3" className="w-8 h-8 rounded-full border-2 border-white" />
              <img src="https://randomuser.me/api/portraits/women/46.jpg" alt="pet4" className="w-8 h-8 rounded-full border-2 border-white" />
            </div>
            <span className="text-[#7A8674] font-medium ml-2">+456 Happy Pets</span>
          </div>
        </div>
        {/* Right: Image */}
        <div className="flex-1 flex justify-center items-center">
          <div className="relative rounded-2xl overflow-hidden bg-[#D9D9D9] w-full max-w-xs aspect-square flex items-center justify-center">
            <img
              src="https://images.unsplash.com/photo-1518717758536-85ae29035b6d?auto=format&fit=facearea&w=400&h=400&facepad=2"
              alt="Groomed pet"
              className="object-cover w-full h-full"
            />
            <span className="absolute top-2 right-2 bg-white rounded-full p-2 shadow text-[#7A8674]">
              <svg width="20" height="20" fill="none" stroke="currentColor" strokeWidth="2" viewBox="0 0 24 24"><circle cx="12" cy="12" r="10" /><path d="M14.31 8l5.74 9.94A10 10 0 0 1 4.26 17.94L10 8m4.31 0A4 4 0 1 1 8 8a4 4 0 0 1 6.31 0z" /></svg>
            </span>
          </div>
        </div>
      </div>
    </div>
  )
}
export default Home

