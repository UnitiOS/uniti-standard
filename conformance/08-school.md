# School

Cases E1 to E3 of the paper test (`uji/01-hitung.md`<!-- ARCHIVE-LINK: ../../01-hitung.md -->
§4.H), written in the reference notation with the core and the calculation
library. E2 is also in [`00-form-examples.md`](00-form-examples.md).

## E1. Weighted final grade

The paper test does not say where the grades for the assignment, the midterm,
and the final exam are read from. Here all three are recorded on one
assessment per student and subject.

```uniti
module paper/e1@v1
  uses uniti/calc@v1

concept Student
concept Subject
concept Assessment

property student : reference Student
property subject : reference Subject
property assignment : number (level)
property midterm : number (level)
property final_exam : number (level)

applies to Assessment:
  student      required
  subject      required
  assignment
  midterm
  final_exam

computed Student.final_grade(subject) : number (level), closed:
  let n = single(all(Assessment, x: x.student = this and x.subject = subject))
  round(0.3 × n.assignment + 0.3 × n.midterm + 0.4 × n.final_exam, 1, nearest)

example final_grade_85
  kind         compute
  title        Final grade, rounded
  explanation  0.3 × 85 + 0.3 × 78 + 0.4 × 90 = 84.9, rounded to 85.
  facts        recorded 20 Dec 2026
    ani   type        Student      valid 1 Jul 2026
    math  type        Subject      valid 1 Jul 2026
    n1    type        Assessment   valid 15 Dec 2026
    n1    student     ani          valid 15 Dec 2026
    n1    subject     math         valid 15 Dec 2026
    n1    assignment  85           valid 15 Dec 2026
    n1    midterm     78           valid 15 Dec 2026
    n1    final_exam  90           valid 15 Dec 2026
  ask          ani.final_grade(math)   T: 20 Dec 2026   R: 20 Dec 2026
  result       85
```

## E2. Class rank, with equal grades

```uniti
module paper/e2@v1

concept Class
concept Student

property class : reference Class
property average_grade : number (level)

applies to Student:
  class        required
  average_grade

computed Student.rank : number (level), closed:
  1 + count(all(Student, s: s.class = this.class
                            and s.average_grade > this.average_grade))

example rank_budi
  kind         compute
  title        The highest grade
  explanation  Budi 88, Ani and Citra 84.9, Dodi 70. No one is above Budi.
  facts        recorded 1 Dec 2026
    c7a    type           Class     valid 1 Jul 2026
    budi   type           Student   valid 1 Jul 2026
    budi   class          c7a       valid 1 Jul 2026
    budi   average_grade  88        valid 1 Dec 2026
    ani    type           Student   valid 1 Jul 2026
    ani    class          c7a       valid 1 Jul 2026
    ani    average_grade  84.9      valid 1 Dec 2026
    citra  type           Student   valid 1 Jul 2026
    citra  class          c7a       valid 1 Jul 2026
    citra  average_grade  84.9      valid 1 Dec 2026
    dodi   type           Student   valid 1 Jul 2026
    dodi   class          c7a       valid 1 Jul 2026
    dodi   average_grade  70        valid 1 Dec 2026
  ask          budi.rank   T: 1 Dec 2026   R: 1 Dec 2026
  result       1

example rank_ani
  kind         compute
  title        Equal grade, equal rank: Ani
  explanation  Only Budi is higher than Ani.
  facts        as in rank_budi
  ask          ani.rank   T: 1 Dec 2026   R: 1 Dec 2026
  result       2

example rank_citra
  kind         compute
  title        Equal grade, equal rank: Citra
  explanation  Citra is equal to Ani, so also rank 2.
  facts        as in rank_budi
  ask          citra.rank   T: 1 Dec 2026   R: 1 Dec 2026
  result       2

example rank_dodi
  kind         compute
  title        Rank after two equal grades
  explanation  Three students are above Dodi, so Dodi is at rank 4, not 3.
  facts        as in rank_budi
  ask          dodi.rank   T: 1 Dec 2026   R: 1 Dec 2026
  result       4
```

## E3. Attendance percentage

The paper test only writes the numbers. Here the number of sessions and the
attendance are recorded as facts, and the result is written as a percentage.

```uniti
module paper/e3@v1
  uses uniti/calc@v1

concept Student

property attended : number (level)
property sessions : number (level)

applies to Student:
  attended
  sessions

computed Student.attendance_percent : number (level), closed:
  round(this.attended ÷ this.sessions, 0.1%, nearest)

example attended_90_of_96
  kind         compute
  title        Attended 90 of 96 sessions
  explanation  90 ÷ 96 = 93.75%, rounded to 0.1% gives 93.8%.
  facts        recorded 20 Dec 2026
    ani   type      Student   valid 1 Jul 2026
    ani   attended  90        valid 20 Dec 2026
    ani   sessions  96        valid 20 Dec 2026
  ask          ani.attendance_percent   T: 20 Dec 2026   R: 20 Dec 2026
  result       93.8%

example attended_77_of_80
  kind         compute
  title        Boundary: exactly half, the previous digit is even
  explanation  77 ÷ 80 = 96.25%. Ordinary rounding goes away from zero: 96.3%.
               Rounding to even would give 96.2%, so this example tells the
               two apart; 93.75% above does not.
  facts        recorded 20 Dec 2026
    budi  type      Student   valid 1 Jul 2026
    budi  attended  77        valid 20 Dec 2026
    budi  sessions  80        valid 20 Dec 2026
  ask          budi.attendance_percent   T: 20 Dec 2026   R: 20 Dec 2026
  result       96.3%
```
