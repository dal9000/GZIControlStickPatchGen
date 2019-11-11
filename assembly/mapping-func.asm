# Preconditions 
# f1 and f2 contain GC raw x and y 

# Constants
.quad 0x0000000000000000 # Zero
.quad 0x3FF0000000000000 # One
.quad 0xBFF0000000000000 # Negative One
.quad 0x3E112E0BE826D695 # Epsilon

.quad 0xBFDA827999F589ED # GC Slope
.quad 0xBFC2492492492492 # N64 Slope
.quad 0x405A800000000000 # GC Stick Max Extent x
.quad 0x405A800000000000 # GC Stick Max Extent -x
.quad 0x405A800000000000 # GC Stick Max Extent y
.quad 0x405A800000000000 # GC Stick Max Extent -y
.quad 0x4054000000000000 # N64 Stick Max Extent
.quad 0x0000000000000000 # Deadzone Radius

# Prelude, we will save registers here

stwu %r1, -0x68(%r1)
stfd %f0, 0x60(%r1)
stfd %f3, 0x58(%r1)
stfd %f4, 0x50(%r1)
stfd %f5, 0x48(%r1)
stfd %f6, 0x40(%r1)
stfd %f7, 0x38(%r1)
stfd %f8, 0x30(%r1)
stfd %f9, 0x28(%r1)
stfd %f29, 0x20(%r1)
stfd %f30, 0x18(%r1)
stfd %f31, 0x10(%r1)
stw %r0, 0x8(%r1)
stw %r3, 0x4(%r1)

# End Prelude

# Constants offset 80005d00
lis %r3, 0x8000
addi %r3, %r3, 0x5d00

lfd %f0, 0x0(%r3)
lfd %f31, 0x58(%r3)

# Apply Custom Deadzone

fabs %f3, %f1
fcmpo %cr0, %f3, %f31
bgt %cr0, xdeadzone
fmuls %f1, %f1, %f0
xdeadzone:

fabs %f3, %f2
fcmpo %cr0, %f3, %f31
bgt %cr0, ydeadzone
fmuls %f2, %f2, %f0
ydeadzone:

# Normalize inputs

# Normalize X

fcmpo %cr0, %f1, %f0
blt normalize_x_neg
lfd %f31, 0x30(%r3)
b normalize_x_end
normalize_x_neg:
lfd %f31, 0x38(%r3)
normalize_x_end:

fdivs %f1, %f1, %f31

# Normalize Y

fcmpo %cr0, %f2, %f0
blt normalize_y_neg
lfd %f31, 0x40(%r3)
b normalize_y_end
normalize_y_neg:
lfd %f31, 0x48(%r3)
normalize_y_end:

fdivs %f2, %f2, %f31

# Fold to upper right triangle

fabs %f3, %f1
fabs %f4, %f2

li %r0, 0x0
fcmpo %cr0, %f4, %f3
bge swap_end
li %r0, 0x1
fmr %f5, %f3
fmr %f3, %f4
fmr %f4, %f5
swap_end:

lfd %f31, 0x18(%r3)
fcmpo %cr0, %f3, %f31
blt done

# Do the mapping

lfd %f31, 0x20(%r3)
lfd %f30, 0x28(%r3)
lfd %f29, 0x8(%r3)

# x in f3, y in f4
# slope = y / x
fdivs %f9, %f4, %f3

# intersect_x in f5
fsubs %f5, %f9, %f31
fres %f5, %f5

# intersect_y in f6
fmadds %f6, %f5, %f31, %f29

# dist_sq1 in f7
fmuls %f5, %f5, %f5
fmadds %f7, %f6, %f6, %f5

# intersect_x in f5 (reused)
fsubs %f5, %f9, %f30
fres %f5, %f5

# intersect_y in f6 (reused)
fmadds %f6, %f5, %f30, %f29

# dist_sq2 in f8
fmuls %f5, %f5, %f5
fmadds %f8, %f6, %f6, %f5

# scale_sq in f5 (intersect_x no longer needed)
fdivs %f5, %f8, %f7

# dist_sq in f6 (intersect_y no longer needed)
fmuls %f3, %f3, %f3
fmadds %f6, %f4, %f4, %f3
fmuls %f6, %f6, %f5

# new_x in f3
fmadds %f3, %f9, %f9, %f29
fdivs %f3, %f6, %f3
frsqrte %f3, %f3
fres %f3, %f3

# new_y in f4
fmuls %f4, %f9, %f3

# Unfold

done:

cmpi %cr0, %r0, 0x0
beq unswap_end
fmr %f5, %f3
fmr %f3, %f4
fmr %f4, %f5
unswap_end:

fcmpo %cr0, %f1, %f0
bge unfold_x
fneg %f1, %f3
b unfold_x_end
unfold_x:
fmr %f1, %f3
unfold_x_end:

fcmpo %cr0, %f2, %f0
bge unfold_y
fneg %f2, %f4
b unfold_y_end
unfold_y:
fmr %f2, %f4
unfold_y_end:

# Denormalize

lfd %f31, 0x50(%r3)
fmuls %f1, %f1, %f31
fmuls %f2, %f2, %f31

# Epilogue, we will restore registers here

lfd %f0, 0x60(%r1)
lfd %f3, 0x58(%r1)
lfd %f4, 0x50(%r1)
lfd %f5, 0x48(%r1)
lfd %f6, 0x40(%r1)
lfd %f7, 0x38(%r1)
lfd %f8, 0x30(%r1)
lfd %f9, 0x28(%r1)
lfd %f29, 0x20(%r1)
lfd %f30, 0x18(%r1)
lfd %f31, 0x10(%r1)
lwz %r0, 0x8(%r1)
lwz %r3, 0x4(%r1)

addi %r1, %r1, 0x68

blr

# End Epilogue
