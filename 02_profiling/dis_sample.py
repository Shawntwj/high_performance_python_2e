import dis 
import julia1_nopil
print(dis.dis(julia1_nopil.calculate_z_serial_purepython))

# more instructions lead to slower code 
# func calls are expensive 