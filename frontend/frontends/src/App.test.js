import { render, screen } from '@testing-library/react';
import App from './App';

test('renders User Management heading', () => {
  render(<App />);
  const heading = screen.getByText(/User Management/i);
  expect(heading).toBeInTheDocument();
});
