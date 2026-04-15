// Component that renders a dropdown of available years
export default function AvailableYears({ onChange }) {
  const years = [2021, 2022, 2023, 2024, 2025, 2026];

  return (
    <select onChange={onChange}>
      {years.map((year) => (
        <option key={year} value={year}>
          {year}
        </option>
      ))}
    </select>
  )
}
