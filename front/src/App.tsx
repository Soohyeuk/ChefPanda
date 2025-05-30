import { Routes, Route } from 'react-router-dom'
import Home from './components/Home/Home'
import PaymentOptions from './components/payment/PaymentOptions'

function App() {
  return (
    <Routes>
      <Route path="/" element={<Home />} />
      <Route path="/payment" element={<PaymentOptions />} />
    </Routes>
  )
}
export default App

