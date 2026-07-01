const LEETCODE_USERNAME = 'PradiptaChandraGiri';
const LC_API = 'https://leetcode.com/graphql';
const query = `
  query($u: String!) {
    allQuestionsCount { difficulty count }
    matchedUser(username: $u) {
      submitStats: submitStatsGlobal {
        acSubmissionNum { difficulty count }
      }
      userCalendar {
        streak
        totalActiveDays
        submissionCalendar
      }
      profile { ranking }
      languageProblemCount { languageName problemsSolved }
    }
  }
`;
fetch(LC_API, {
  method: 'POST',
  headers: { 'Content-Type': 'application/json', 'Referer': 'https://leetcode.com' },
  body: JSON.stringify({ query, variables: { u: LEETCODE_USERNAME } })
})
.then(r => r.json())
.then(d => console.log(JSON.stringify(d, null, 2)))
.catch(e => console.error(e));
