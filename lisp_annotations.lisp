; (define (name arg1 arg2 ...) body): function defition
; (let (name val) body): variable defintion
; (eq arg1 arg2): equality
; (zeros_like arg1): np.zeros_like
; (index arg1 arg2 arg3): index using the arg2+ into the array at arg1
; (array_assign arg1 arg2)


(define (func1_25d8a9c8 grid)
	(let (row_mask (logical_and
			(eq (index grid :, 0) (index grid :, 1))
			(eq (index grid :, 1) (index grid :, 2))))
		(array_assign (zeros_like grid) row_mask : 5)
	)
)

