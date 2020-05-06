import os
import matplotlib.pyplot as plt
import matplotlib.colors as colors
from matplotlib import ticker, cm
import numpy


class dirac_plot:

  @staticmethod
  def run():
    cx, cy, cz = 0, 0, 0
    x_last, y_last, z_last = None, None, None
    fh = open('plot.3d.scalar', 'r')
    for line in fh:
      line = dirac_plot.one_space(line.strip()," ")
      f = line.split(" ")   
      if(x_last == None or f[0] != x_last):
        cx = cx + 1
      if(cx == 1 and (y_last == None or f[1] != y_last)):
        cy = cy + 1
      if(cy == 1 and (y_last == None or f[2] != z_last)):
        cz = cz + 1
      x_last, y_last, z_last = f[0], f[1], f[2]
    fh.close()
    

    d = numpy.zeros((cx,cy,cz,4,),)

    x, y, z = 0, 0, 0
    x_last, y_last, z_last = None, None, None
    fh = open('plot.3d.scalar', 'r')
    for line in fh:
      line = dirac_plot.one_space(line.strip()," ")

      f = line.split(" ")      

      d[x, y, z, 0] = float(f[0])
      d[x, y, z, 1] = float(f[1])
      d[x, y, z, 2] = float(f[2])
      d[x, y, z, 3] = float(f[3])

      # update
      z = (z + 1) % cz
      if(z == 0):
        y = (y + 1) % cy 
      if(z == 0 and y == 0):
        x = x + 1
    fh.close()

    mn=numpy.min(d[:, :, :, 3])
    mx=numpy.max(d[:, :, :, 3])

    x_v = d[:, 0, 0, 0]
    y_v = d[0, :, 0, 1]
    z_v = d[0, 0, :, 2]


    dirac_plot.make_dir('pngs')
    dirac_plot.make_dir('eps')

    plt.figure(num=None, figsize=(19.20, 10.80), dpi=100)

    p = 0
    for xi in range(cx):
      p = p + 1
      plt.clf()   
      plt.title("YZ-plane")
      pcm = plt.contourf(y_v, z_v, d[xi, :, :, 3], norm=colors.LogNorm(vmin=mn, vmax=mx), cmap='viridis')
      plt.colorbar(pcm, extend='max')
      fn_p = str(p)
      while(len(fn_p) < 4):
        fn_p = '0' + fn_p
      fn = str(xi + 1)
      while(len(fn) < 4):
        fn = '0' + fn
      plt.savefig('pngs/v_' + fn_p + '.png', format='png')
      plt.savefig('eps/x_' + fn + '.eps', format='eps')

    for yi in range(cy):
      p = p + 1
      plt.clf()    
      plt.title("XZ-plane")
      pcm = plt.contourf(x_v, z_v, d[:, yi, :, 3], norm=colors.LogNorm(vmin=mn, vmax=mx), cmap='viridis')
      plt.colorbar(pcm, extend='max')
      fn_p = str(p)
      while(len(fn_p) < 4):
        fn_p = '0' + fn_p
      fn = str(yi + 1)
      while(len(fn) < 4):
        fn = '0' + fn
      plt.savefig('pngs/v_' + fn_p + '.png', format='png')
      plt.savefig('eps/y_' + fn + '.eps', format='eps')

    for zi in range(cz):
      p = p + 1
      plt.clf()    
      plt.title("XY-plane")
      pcm = plt.contourf(x_v, y_v, d[:, :, zi, 3], norm=colors.LogNorm(vmin=mn, vmax=mx), cmap='viridis')
      plt.colorbar(pcm, extend='max')
      fn_p = str(p)
      while(len(fn_p) < 4):
        fn_p = '0' + fn_p
      fn = str(zi + 1)
      while(len(fn) < 4):
        fn = '0' + fn
      plt.savefig('pngs/v_' + fn_p + '.png', format='png')
      plt.savefig('eps/z_' + fn + '.eps', format='eps')
    os.system("ffmpeg -r 15 -i pngs/v_%04d.png -c:v libx264 -vf fps=30 -pix_fmt yuv420p video.mp4")

    exit()



  @staticmethod
  def one_space(line, sep=" "):
    out = ''   
    indata = 0
    last_char = None
    for char in line:
      if(indata == 1 and char != "'" and last_char != "\\"):
        out = out + char
      elif(indata == 1 and char == "'" and last_char != "\\"):
        out = out + char
        indata = 0
      elif(indata == 2 and char != '"' and last_char != "\\"):
        out = out + char
      elif(indata == 2 and char == '"' and last_char != "\\"):
        out = out + char
        indata = 0
      elif(indata == 0 and not (char == " " and last_char == " ")):
        out = out + char
      last_char = char
    return out   


  @staticmethod
  def make_dir(dir):
    try:
      if(not os.path.exists(dir) and dir.strip() != ''):
        os.mkdir(dir) 
        return True
      return False
    except:
      return False
    
    
dirac_plot.run()

