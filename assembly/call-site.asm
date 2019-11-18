xoris %r0, %r20, 0x8000
stw %r0, 0x44(%r1)
lfd %f1, 0x40(%r1)
fsubs %f1, %f1, %f25

xoris %r0, %r19, 0x8000
stw %r0, 0x4c(%r1)
lfd %f2, 0x48(%r1)
fsubs %f2, %f2, %f25

# Branch will go here
.long 0x00000000

fctiw %f0, %f1
stfd %f0, 0x78(%r1)
lwz %r20, 0x7c(%r1)

fctiw %f0, %f2
stfd %f0, 0x78(%r1)
lwz %r19, 0x7c(%r1)

b 0x84

