def pref_to_inf(exp):
  if not isinstance(exp, str):
    print("Ошибка! Тип даных должен быть String!")
    return exp
  exp = exp.split()
  variants = ['+', '-', '*', '/']
  for e in exp:
    if not (e.isnumeric() or e in variants):
      print("Ошибка! Пишите в строке только (числа, *, /, +, -)!")
      return " ".join(exp)
  symbols = []
  i = 0
  while True:
    if len(exp) < 3 and len(symbols) == 0:
      print("Ошибка! Слишком короткое выражение:", " ".join(exp))
      return " ".join(exp)
    if (i == 0 and exp[i] in variants) or (i > 0 and exp[i - 1] in variants and exp[i] in variants):
      symbols.append(exp.pop(i))
    elif i > 0 and exp[i - 1].isnumeric() and exp[i].isnumeric() and len(symbols) == 0:
      print("Ошибка! Мест для знаков больше, чем самих знаков:", " ".join(exp))
      return " ".join(exp)
    elif i > 0 and exp[i - 1].isnumeric() and exp[i].isnumeric():
      exp.insert(i, symbols.pop(0))
    else:
      i += 1
    if len(exp) <= i and len(symbols) > 0:
      print("Ошибка! Знаков больше, чем мест для них:", " ".join(exp), " ".join(symbols))
      return " ".join(exp) + " " + " ".join(symbols)
    if len(exp) <= i:
      print("Инфиксная запись:", " ".join(exp))
      return " ".join(exp)

#ret = pref_to_inf(str(input("Введите выражения в префиксной нотации (разделяйте числа и знаки пробелами):\n")))