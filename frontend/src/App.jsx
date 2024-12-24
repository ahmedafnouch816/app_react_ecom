// App.jsx
import { Route, Routes, BrowserRouter } from 'react-router-dom';
import Index from './views/core';
import MainWrapper from '../src/layouts/MainWrapper';

function App() {
  return (
    <>
      <BrowserRouter>
        <MainWrapper>
          <Routes>
            <Route path="/" element={<Index />} />
          </Routes>
        </MainWrapper>
      </BrowserRouter>
    </>
  );
}

export default App;

