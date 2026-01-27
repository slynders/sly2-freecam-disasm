.set noreorder /* we dont need no stinking reordering. */
.set noat

.data
.global meosCamFlag0
meosCamFlag0:
    .byte 0
.global meosCamFlag1
meosCamFlag1:
    .byte 0
.global meosCamPauseFlag
meosCamPauseFlag:
    .byte 0
.global meosCamDisableHudFlag
meosCamDisableHudFlag:
    .byte 0
.global meosCamFlag4
meosCamFlag4:
    .byte 0
