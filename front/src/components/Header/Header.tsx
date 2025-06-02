import React from 'react'
import logo from '@/assets/chef_panda.svg'
import { Link } from 'react-router-dom'
import { Button } from '@/components/ui/button'

const Header : React.FC = () => {
  return (
    <div className="flex w-full h-24 justify-center items-center bg-yellow-500">
        <div className="flex w-3/4 h-24 justify-between items-center">
            <div className="flex h-full justify-between items-center">
                <img src={logo} alt="logo" className="w-13 h-13" />
            </div>
            <div className="flex w-1/5 h-full justify-between items-center">
                    <Link to="/">Home</Link>
                    <Link to="/about">About</Link>
                    <Link to="/contact">Contact</Link>
                    <Link to="/recipes">Recipes</Link>
                    <Link to="/pricing">Pricing</Link>
            </div>
            <div className="flex h-full justify-between items-center">
                <Button className="bg-green-800 text-white hover:opacity-90 border-black/30" variant="outline">
                    <Link to="/login">Login</Link>
                </Button>
            </div>
        </div>
    </div>
  )
}

export default Header
