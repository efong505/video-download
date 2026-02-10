# 10-Candidate Chunk Structure for New Jersey

## Total: 150 candidates = 15 chunks of 10 each

### Chunk Breakdown:

**CHUNK_2A (1-10): Federal - U.S. Senate + House Districts 1-3**
1. Cory Booker (D) - U.S. Senate
2. Curtis Bashaw (R) - U.S. Senate
3. Christina Khalil (Green) - U.S. Senate
4. Kenneth Kaplan (Libertarian) - U.S. Senate
5. Donald Norcross (D) - U.S. House District 1
6. Teddy Liddell (R) - U.S. House District 1
7. Joe Salerno (D) - U.S. House District 2
8. Jeff Van Drew (R) - U.S. House District 2
9. Herb Conaway (D) - U.S. House District 3
10. Rajesh Mohan (R) - U.S. House District 3

**CHUNK_2B (11-20): Federal - House Districts 4-8**
11. Matthew Jenkins (D) - U.S. House District 4
12. Chris Smith (R) - U.S. House District 4
13. Josh Gottheimer (D) - U.S. House District 5
14. Mary Jo-Ann Guinchard (R) - U.S. House District 5
15. Frank Pallone (D) - U.S. House District 6
16. Scott Fegler (R) - U.S. House District 6
17. Sue Altman (D) - U.S. House District 7
18. Thomas Kean Jr. (R) - U.S. House District 7
19. Rob Menendez (D) - U.S. House District 8
20. Anthony Valdes (R) - U.S. House District 8

**CHUNK_2C (21-30): Federal - House Districts 9-12 + Governor**
21. Bill Pascrell (D) - U.S. House District 9
22. Billy Prempeh (R) - U.S. House District 9
23. Donald Payne Jr. (D) - U.S. House District 10
24. Carmen Bucco (R) - U.S. House District 10
25. Mikie Sherrill (D) - U.S. House District 11
26. Joseph Belnome (R) - U.S. House District 11
27. Bonnie Watson Coleman (D) - U.S. House District 12
28. Darius Mayfield (R) - U.S. House District 12
29. Jack Ciattarelli (R) - Governor
30. Mikie Sherrill (D) - Governor

**CHUNK_2D (31-40): Governor + Assembly Districts 1-4**
31. Ras Baraka (D) - Governor (DROPPED OUT)
32. Steve Fulop (D) - Governor (DROPPED OUT)
33. Bill Spadea (R) - Governor (DROPPED OUT)
34. Jon Bramnick (R) - Governor (DROPPED OUT)
35. Erik K. Simonsen (R) - Assembly District 1 Seat 1
36. Carolyn Rush (D) - Assembly District 1 Seat 1
37. Antwan McClellan (R) - Assembly District 1 Seat 2
38. Maureen Rowan (D) - Assembly District 1 Seat 2
39. Don Guardian (R) - Assembly District 2 Seat 1
40. Heather Simmons (D) - Assembly District 2 Seat 1

**CHUNK_2E (41-50): Assembly Districts 2-5**
41. Claire Swift (R) - Assembly District 2 Seat 2
42. Chris Konawel (D) - Assembly District 2 Seat 2
43. Dave Bailey Jr. (D) - Assembly District 3 Seat 1
44. Dan Hutchison (D) - Assembly District 3 Seat 1
45. Bethanne McCarthy Patrick (R) - Assembly District 3 Seat 2
46. Amanda Esposito (R) - Assembly District 3 Seat 2
47. William F. Moen Jr. (D) - Assembly District 4 Seat 1
48. Cody D. Miller (D) - Assembly District 4 Seat 2
49. Constance Ditzel (R) - Assembly District 4
50. Louis D. Greenwald (D) - Assembly District 5 Seat 1

**CHUNK_2F (51-60): Assembly Districts 5-7**
51. Nilsa I. Cruz-Perez (D) - Assembly District 5 Seat 2
52. John M. Brangan (R) - Assembly District 5
53. Pamela R. Lampitt (D) - Assembly District 6 Seat 1
54. Carol Murphy (D) - Assembly District 6 Seat 2
55. Dione Johnson (R) - Assembly District 6
56. Herb Conaway (D) - Assembly District 7 Seat 1
57. Andrea Katz (D) - Assembly District 7 Seat 2
58. Michael Torrissi Jr. (R) - Assembly District 7
59. Brian E. Rumpf (R) - Assembly District 8 Seat 1
60. Lisa Bennett (D) - Assembly District 8 Seat 1

**CHUNK_2G (61-70): Assembly Districts 8-10**
61. Greg Myhre (R) - Assembly District 8 Seat 2
62. Janine G. Bauer (D) - Assembly District 8 Seat 2
63. Paul Kanitra (R) - Assembly District 9 Seat 1
64. John Catalano (R) - Assembly District 9 Seat 2
65. Gregory P. McGuckin (R) - Assembly District 9
66. Margie Donlon (D) - Assembly District 10 Seat 1
67. Luanne M. Peterpaul (D) - Assembly District 10 Seat 2
68. Margaret M. Donlon (D) - Assembly District 10
69. Andrew C. Wardell (R) - Assembly District 10
70. Kyler Dineen (R) - Assembly District 10

**CHUNK_2H (71-80): Assembly Districts 11-13**
71. Robert D. Clifton (R) - Assembly District 11 Seat 1
72. Alex Sauickie (R) - Assembly District 11 Seat 2
73. Victoria A. Flynn (R) - Assembly District 12 Seat 1
74. Gerard P. Scharfenberger (R) - Assembly District 12 Seat 2
75-80. [Continue Assembly Districts 13-14]

**CHUNK_2I (81-90): Assembly Districts 15-17**

**CHUNK_2J (91-100): Assembly Districts 18-20**

**CHUNK_2K (101-110): School Boards - Newark, Jersey City, Paterson**

**CHUNK_2L (111-120): School Boards - Elizabeth, Edison, Woodbridge**

**CHUNK_2M (121-130): School Boards - Camden, Trenton, Clifton**

**CHUNK_2N (131-140): School Boards - Passaic, Union City, Bayonne**

**CHUNK_2O (141-150): School Boards - East Orange, Vineland, New Brunswick**

---

## Usage Instructions:

1. Run CHUNK_2A through Grok → Save to `chunk2a_output.txt`
2. Run CHUNK_2B through Grok → Save to `chunk2b_output.txt`
3. Continue through CHUNK_2O
4. Combine all 15 files using `combine_nj_chunks.py`

**Each chunk = ~5,000 tokens (manageable for Grok)**
