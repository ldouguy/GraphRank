from collections import defaultdict
import json

class AssocBuilder:
	def __init__(self, CAPI=None, SAPI=None, assocFile=None):
		self._unlinked = set()
		if CAPI:
			self._unlinked |= set(CAPI.playerDict.values())
		if SAPI:
			self._unlinked |= set(SAPI.playerDict.values())

		self._linked = set()
		self.assoc = {}
		#assocIdx is the reverse of assoc, converted to indices
		self._assocIdx = defaultdict(list)
		self._tagList = {i: tag for i, tag in enumerate(sorted(list(self._unlinked), key=lambda string: str(string).lower()))}

		if assocFile:
			with open(assocFile) as assocdata:
				preassoc = json.load(assocdata)
			pairs = []
			rDict = {self._tagList[i]: i for i in self._tagList}
			for tag in preassoc:
				if tag in self._unlinked:
					pairs.append((rDict[tag], rDict[preassoc[tag]]))

			self._link(pairs)

		self._print()
		self._match()

	def _match(self):
		linkstate = 0
		while True:
			if linkstate:
				cmdstr = raw_input("Enter pairs of indices, separated by semicolons (eg. 0 5; 7 2)\nOr type 'done' to enter more commands.\n>>> ")
				if cmdstr:
					if str(cmdstr.strip()).lower() == "done":
						linkstate = 0
					else:
						try:
							cmdarr = cmdstr.split(';')
							for i, cmd in enumerate(cmdarr):
								cmdarr[i] = cmd.split()
								for j in range(len(cmdarr[i])):
									cmdarr[i][j] = int(cmdarr[i][j])
							self._link(cmdarr)
						except:
							print "Your command has incorrect syntax. Please try again."

			else:
				cmdstr = raw_input("Enter your command. Type 'help' for instructions.\n>>> ")
				cmdarr = cmdstr.split()
				if cmdarr:
					cmd = cmdarr[0]
					if len(cmdarr) == 1:
						if cmd == "link":
							linkstate = 1
						elif cmd == "suggest":
							self._suggest()
						elif cmd == "print":
							self._print()
						elif cmd == "help":
							self._help()
						elif cmd == "apply":
							yesno = raw_input("Are you sure you'd like to continue? (y to confirm)\n>>> ")
							if yesno == "y":
								self._apply()
						elif cmd == "exit":
							yesno = raw_input("Are you sure you'd like to exit? (y to confirm)\n>>> ")
							if yesno == "y":
								break

					elif cmd == "unlink":
						try:
							for i in range(1, len(cmdarr)):
								cmdarr[i] = int(cmdarr[i])
							self._unlink(cmdarr[1:])
						except:
							print "Your command has incorrect syntax. Please enter another command."
					elif cmd == "set":
						try:
							for i in range(1, len(cmdarr)):
								cmdarr[i] = int(cmdarr[i])
							self._set(cmdarr[1:])
						except:
							print "Your command has incorrect syntax. Please enter another command."
					elif not cmd:
						pass
					else:
						print "Invalid command entered. Try again."

	def _link(self, pairs):
		for i, j in pairs:
			if i not in self._tagList:
				print i, " is not a valid index"
			if j not in self._tagList:
				print j, " is not a valid index"
			if i in self._tagList and j in self._tagList:
				self._unlinked.discard(self._tagList[i])
				self._unlinked.discard(self._tagList[j])
				self.assoc[self._tagList[i]] = self._tagList[j]
				self._assocIdx[j].append(i)
				self._linked.add(self._tagList[i])
				print i, "linked to", j

	def _unlink(self, idxs):
		for i in idxs:
			if i in self._tagList:
				self._linked.discard(self._tagList[i])
				del self.assoc[self._tagList[i]]
				self._assocIdx[j].remove(i)
			else:
				print i, " is not a valid index"

	def _apply(self):
		remove = set()
		for i in self._tagList:
			if self._tagList[i] in self._linked:
				remove.add(i)

		self._linked -= set([self._tagList[i] for i in remove])
		for i in remove:
			del self._tagList[i]

	def _suggest(self):
		pass

	def _print(self):
		print "Index:" + " " + "Tag" + " "*17 + "Linked By" + " "*11 + "Verified"
		print "="*58
		for i in self._assocIdx:
			if i in self._tagList:
				print "%-*d: %-*s %-*s **" % (5, i, 20, self._tagList[i], 20, ", ".join([str(j) for j in self._assocIdx[i]]))
		for i in self._tagList:
			if i not in self._assocIdx:
				print "%-*d: %-*s %-*s" % (5, i, 20, self._tagList[i], 20, "")

	def _set(self, idxs):
		for i in idxs:
			if i in self._tagList:
				self._assocIdx[i] = []
			else:
				print i, " is not a valid index"

	def _help(self):
		print "\nlink:"
		print "\nunlink:"
		print "\napply:"
		print "\nprint:"
		print "\nset:"
		print "\n>>> "
		pass

	###########################

	def save_to_json(self, outfile="assoc.json"):
		with open(outfile, "w") as out:
			json.dump(self.assoc, out, indent=2)