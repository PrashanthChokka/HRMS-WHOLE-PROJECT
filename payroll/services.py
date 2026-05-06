def calculate_salary(basic, leave_days):

    per_day = basic / 30
    leave_deduction = per_day * leave_days

    hra = basic * 0.20
    allowances = basic * 0.10
    bonus = 0

    gross = basic + hra + allowances + bonus

    # PF
    pf = basic * 0.12

    # ✅ NEW TAX RULE
    if gross > 100000:
        tax = gross * 0.10
    else:
        tax = 0

    net = gross - (leave_deduction + pf + tax)

    return {
        "hra": hra,
        "allowances": allowances,
        "bonus": bonus,
        "leave_deduction": leave_deduction,
        "pf": pf,
        "tax": tax,
        "gross": gross,
        "net": net
    }