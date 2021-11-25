import matplotlib.pyplot as plt
  
earning = []
counts = []

  
f = open('demofile2.txt','r')
x = list(f)
plt.plot(list(map(lambda i: float(i[:-1].replace(",","")),x)))
plt.ylabel('earnings')
plt.show()
