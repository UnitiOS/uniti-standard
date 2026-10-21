# Payroll

Cases G1 to G3 from the paper test (`uji/01-hitung.md`<!-- ARCHIVE-LINK: ../../01-hitung.md -->
§4.D), written in the reference notation with the core and the calculation
library. The tax brackets and the overtime rule here are content examples, not
tax or labor provisions.

## G1. Progressive income tax

The tax brackets are recorded as facts. The top bracket has no upper limit.

```uniti
module paper/g1@v1

concept Employee
concept TaxTable
concept TaxBracket

property taxable_income : number (money, position)
property tax_table : reference TaxTable
property table : reference TaxTable
property lower_limit : number (money, position)
property upper_limit : number (money, position)
property rate : number (position)

applies to Employee:
  taxable_income
  tax_table    required

applies to TaxBracket:
  table        required
  lower_limit  required
  upper_limit
  rate         required

computed Employee.annual_tax : number (money, increase), closed:
  let ti = this.taxable_income
  sum(all(TaxBracket, l: l.table = this.tax_table),
      l: max(0, (if exists(l.upper_limit) then min(ti, l.upper_limit)
                 else ti) − l.lower_limit) × l.rate)

example tax_three_brackets
  kind         compute
  title        Tax on an income of 300 million
  explanation  60 million × 5% + 190 million × 15% + 50 million × 25% =
               3,000,000 + 28,500,000 + 12,500,000 = 44,000,000. The bracket
               above 500 million is not used.
  zone         WIB
  facts        recorded 2 Jan 2026 09:00
    tp    type         TaxTable         valid 1 Jan 2026
    l1    type         TaxBracket       valid 1 Jan 2026
    l1    table        tp               valid 1 Jan 2026
    l1    lower_limit  0 IDR            valid 1 Jan 2026
    l1    upper_limit  60,000,000 IDR   valid 1 Jan 2026
    l1    rate         5%               valid 1 Jan 2026
    l2    type         TaxBracket       valid 1 Jan 2026
    l2    table        tp               valid 1 Jan 2026
    l2    lower_limit  60,000,000 IDR   valid 1 Jan 2026
    l2    upper_limit  250,000,000 IDR  valid 1 Jan 2026
    l2    rate         15%              valid 1 Jan 2026
    l3    type         TaxBracket       valid 1 Jan 2026
    l3    table        tp               valid 1 Jan 2026
    l3    lower_limit  250,000,000 IDR  valid 1 Jan 2026
    l3    upper_limit  500,000,000 IDR  valid 1 Jan 2026
    l3    rate         25%              valid 1 Jan 2026
    l4    type         TaxBracket       valid 1 Jan 2026
    l4    table        tp               valid 1 Jan 2026
    l4    lower_limit  500,000,000 IDR  valid 1 Jan 2026
    l4    rate         30%              valid 1 Jan 2026
    budi  type                  Employee          valid 1 Jan 2026
    budi  tax_table             tp                valid 1 Jan 2026
    budi  taxable_income        300,000,000 IDR   valid 1 Jan 2026
  ask          budi.annual_tax   T: 31 Dec 2026   R: 31 Dec 2026
  result       44,000,000 IDR
```

## G2. Daily overtime

Working hours are recorded as a duration, so the limit of 8 is written
`8 hours`, and the wage has the unit IDR/hour.

```uniti
module paper/g2@v1

concept Employee
concept Contract
concept Attendance

property contract : reference Contract
property hourly_wage : number (money/duration, position)
property employee : reference Employee
property date : date
property hours : number (duration, position)

applies to Employee:
  contract     required

applies to Contract:
  hourly_wage  required

applies to Attendance:
  employee     required
  date         required
  hours        required

computed Employee.overtime_pay(period) : number (money, increase), closed:
  sum(all(Attendance, h: h.employee = this and h.date in period),
      h: max(0, h.hours − 8 hours) × 1.5 × at(h.date, this.contract.hourly_wage))

example overtime_one_week
  kind         compute
  title        One week of overtime
  explanation  Working hours 8, 10, 9, 8, 11. Overtime 0 + 2 + 1 + 0 + 3 = 6
               hours; 6 × 1.5 × 50,000 = 450,000.
  zone         WIB
  facts        recorded 9 Oct 2026 18:00
    budi  type          Employee          valid 1 Jan 2026
    budi  contract      kb                valid 1 Jan 2026
    kb    type          Contract          valid 1 Jan 2026
    kb    hourly_wage   50,000 IDR/hour   valid 1 Jan 2026
    h1    type          Attendance        valid 5 Oct 2026
    h1    employee      budi              valid 5 Oct 2026
    h1    date          5 Oct 2026        valid 5 Oct 2026
    h1    hours         8 hours           valid 5 Oct 2026
    h2    type          Attendance        valid 6 Oct 2026
    h2    employee      budi              valid 6 Oct 2026
    h2    date          6 Oct 2026        valid 6 Oct 2026
    h2    hours         10 hours          valid 6 Oct 2026
    h3    type          Attendance        valid 7 Oct 2026
    h3    employee      budi              valid 7 Oct 2026
    h3    date          7 Oct 2026        valid 7 Oct 2026
    h3    hours         9 hours           valid 7 Oct 2026
    h4    type          Attendance        valid 8 Oct 2026
    h4    employee      budi              valid 8 Oct 2026
    h4    date          8 Oct 2026        valid 8 Oct 2026
    h4    hours         8 hours           valid 8 Oct 2026
    h5    type          Attendance        valid 9 Oct 2026
    h5    employee      budi              valid 9 Oct 2026
    h5    date          9 Oct 2026        valid 9 Oct 2026
    h5    hours         11 hours          valid 9 Oct 2026
  ask          budi.overtime_pay(range(5 Oct 2026, 12 Oct 2026))   T: 11 Oct 2026   R: 11 Oct 2026
  result       450,000 IDR
```

## G3. A raise in the middle of the month

The salary is first summed per part of the month, then rounded once at the end
with `round` from the library.

```uniti
module paper/g3@v1
  uses uniti/calc@v1

concept Employee
concept Contract

property contract : reference Contract
property monthly_salary : number (money, position)

applies to Employee:
  contract     required

applies to Contract:
  monthly_salary  required

computed Employee.salary(month) : number (money, increase), closed:
  round(sum(history(this.contract.monthly_salary, in: month),
            r: r.value × span(overlap(r.range, month), day)
               ÷ span(month, day)),
        1 IDR, nearest)

example october_salary
  kind         compute
  title        October salary with a raise on 16 October
  explanation  9,000,000 × 15/31 + 9,300,000 × 16/31 = 4,354,838.709… +
               4,800,000 = 9,154,838.709…, rounded to 9,154,839.
  zone         WIB
  facts        recorded 1 Oct 2026 09:00
    budi     type            Employee        valid 1 Jan 2026
    budi     contract        kb              valid 1 Jan 2026
    kb       type            Contract        valid 1 Jan 2026
    f1: kb   monthly_salary  9,000,000 IDR   valid 1 Jan 2026
    f2: kb   monthly_salary  9,300,000 IDR   valid 16 Oct 2026   replaces f1
  ask          budi.salary(range(1 Oct 2026, 1 Nov 2026))   T: 31 Oct 2026   R: 1 Nov 2026
  result       9,154,839 IDR
```
