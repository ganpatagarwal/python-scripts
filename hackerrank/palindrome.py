from collections import deque
import sys

class Solution:
    # Write your code here
    def __init__(self):
        self.queue = deque()
        self.stack = deque()

    def pushCharacter(self, char):
        self.stack.append(char)

    def enqueueCharacter(self, char):
        self.queue.append(char)

    def popCharacter(self):
        print(self.stack)
        return self.stack.pop()

    def dequeueCharacter(self):
        print(self.queue)
        return self.queue.popleft()

# read the string s
s = input("provide :")
# Create the Solution class object
obj = Solution()

l = len(s)
# push/enqueue all the characters of string s to stack
for i in range(l):
    obj.pushCharacter(s[i])
    obj.enqueueCharacter(s[i])

isPalindrome = True
'''
pop the top character from stack
dequeue the first character from queue
compare both the characters
'''
for i in range(l // 2):
    # print(obj.popCharacter())
    # print(obj.dequeueCharacter())
    if obj.popCharacter() != obj.dequeueCharacter():
        isPalindrome = False
        print("False")
        break
# finally print whether string s is palindrome or not.
if isPalindrome:
    print("The word, " + s + ", is a palindrome.")
else:
    print("The word, " + s + ", is not a palindrome.")