# COCOMO Estimation Tool — Mini Project Report

## 1. Aim

To apply quantitative software project estimation techniques and develop a
COCOMO Estimation Tool that accepts Lines of Code (LoC) as input and produces
effort, development time and staffing estimates for different COCOMO models.

## 2. Objective

The objectives are:

1. Convert project size from LoC to KLoC.
2. Implement Basic COCOMO.
3. Implement Intermediate COCOMO using an Effort Adjustment Factor (EAF).
4. Implement Detailed COCOMO with phase-wise effort distribution.
5. Compare estimates for Organic, Semi-Detached and Embedded project modes.
6. Present the results using a simple graphical interface.

## 3. Theory

COCOMO stands for Constructive Cost Model. It is a software estimation model
used to estimate development effort and schedule from software size.

The project size is generally represented in KLoC:

KLoC = LoC / 1000

### Basic COCOMO

Effort = a × (KLoC)^b

Development Time = c × (Effort)^d

Average Staff = Effort / Development Time

### Coefficients

| Mode | a | b | c | d |
|---|---:|---:|---:|---:|
| Organic | 2.4 | 1.05 | 2.5 | 0.38 |
| Semi-Detached | 3.0 | 1.12 | 2.5 | 0.35 |
| Embedded | 3.6 | 1.20 | 2.5 | 0.32 |

### Intermediate COCOMO

Intermediate COCOMO introduces an Effort Adjustment Factor (EAF):

Effort = a × (KLoC)^b × EAF

The EAF represents the combined effect of cost-driver ratings.

### Detailed COCOMO

Detailed COCOMO further distributes the estimated effort over software
engineering phases such as requirements/planning, design, coding/testing and
integration/testing.

## 4. Algorithm

1. Start.
2. Accept Lines of Code from the user.
3. If the input is in LoC, convert it to KLoC.
4. Accept EAF for Intermediate/Detailed COCOMO.
5. For each project mode:
   - Read coefficients a, b, c and d.
   - Calculate effort.
   - Calculate development time.
   - Calculate average staffing.
6. Display Basic COCOMO results.
7. Display Intermediate COCOMO results.
8. Distribute Detailed COCOMO effort across phases.
9. Display comparison charts.
10. Stop.

## 5. Sample Calculation

Assume:

LoC = 10,000

Therefore:

KLoC = 10

For Organic Basic COCOMO:

Effort = 2.4 × (10)^1.05

Development Time = 2.5 × (Effort)^0.38

Average Staff = Effort / Development Time

The application performs these calculations automatically and displays the
result with appropriate rounding.

## 6. Software Requirements

- Python 3.x
- Streamlit
- Pandas
- Matplotlib
- Web browser

## 7. Hardware Requirements

- Any modern computer
- Minimum 4 GB RAM recommended
- Internet is only required for installing Python packages; the calculator
  itself runs locally.

## 8. Expected Outcome

The developed tool accepts LoC and provides:

- Estimated effort in person-months
- Estimated development time in months
- Average number of personnel
- Basic COCOMO results
- Intermediate COCOMO results
- Detailed phase-wise effort
- Graphical comparison

## 9. Advantages

- Easy to use
- Fast calculations
- Reduces manual calculation errors
- Supports multiple project modes
- Provides visual comparison
- Can be extended with cost-driver inputs

## 10. Limitations

- EAF is entered directly rather than calculated from individual cost-driver
  ratings.
- The tool uses a classical COCOMO formulation.
- Detailed COCOMO phase percentages are educational approximations and should
  be replaced by the percentages specified in the course reference if
  required.

## 11. Future Scope

The tool can be extended with:

- Full Intermediate COCOMO cost-driver questionnaire
- COCOMO II
- Project cost estimation using salary/cost per person-month
- Export to PDF/CSV
- Multiple project scenarios
- Database storage
- Interactive dashboards

## 12. Conclusion

The COCOMO Estimation Tool demonstrates how quantitative software estimation
can be automated. By providing LoC as input, the application calculates effort,
development time and staffing estimates for different project modes and
COCOMO approaches. The graphical interface makes the results easier to
understand and compare.
