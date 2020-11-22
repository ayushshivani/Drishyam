import random

class Schnorr:
	'''
	This class simulates the POV of the Prover.
	'''

	def __init__(self):
		self.p = int(1e6 + 3)
		self._w = random.randint(0, self.p - 1)
		self.g = 16
		self.h = pow(self.g, self._w, self.p)
		self.m = self.p - 1

	def offer(self):
		'''
		Prover sends t in Zm and sends y = g ^ t mod p to Verifier V
		'''
		t = random.randint(0, self.m)
		y = pow(self.g, t, self.p)
		self.t = t
		return y

	def challenge(self, c):
		'''
		Verifier V selects c in Zm and sends c to P
		'''
		self.c = c

	def response(self):
		'''
		'''
		s = (self.t + self._w * self.c) % self.m
		return int(s)

if __name__ == "__main__":
	'''
	Simulating the verifier
	'''
	prover = Schnorr()
	y = prover.offer()
	print("Prover offered y = {} to Verifier.".format(y))
	c = random.randint(0, prover.m)
	# c = 21
	prover.challenge(c)
	print("Verifier challenged Prover with c = {}.".format(c))
	s = prover.response()
	print("Verifier received s = {} from prover".format(s))
	LHS = pow(prover.g, s, prover.p)
	print("g ^ s mod p = {}".format(LHS))
	some_num = pow(prover.h, c)

	RHS = int((y * some_num) % prover.p)
	print("y * h^c mod p = {}".format(RHS))
	print("Are the above same ? ")
	if LHS == RHS:
		print("Yes, Verified")
	else:
		print("No, Not verified")




