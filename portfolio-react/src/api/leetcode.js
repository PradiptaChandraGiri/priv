import api from './axios';

export const fetchLeetCodeProfile = async (username) => {
  const query = `
    query getUserProfile($username: String!) {
      allQuestionsCount { difficulty count }
      matchedUser(username: $username) {
        username
        submitStats: submitStatsGlobal { acSubmissionNum { difficulty count submissions } }
        profile { ranking userAvatar realName aboutMe school websites countryName company jobTitle skillTags postViewCount postViewCountDiff reputation reputationDiff solutionCount solutionCountDiff categoryDiscussCount categoryDiscussCountDiff }
        badges { id displayName icon creationDate }
        activeBadge { id displayName icon }
        userCalendar { activeYears streak totalActiveDays dccBadges { timestamp badge { name icon } } submissionCalendar }
        languageProblemCount { languageName problemsSolved }
        tagProblemCounts {
          advanced { tagName tagSlug problemsSolved }
          intermediate { tagName tagSlug problemsSolved }
          fundamental { tagName tagSlug problemsSolved }
        }
      }
    }
  `;

  const response = await api.post('/leetcode-proxy', { query, variables: { username } });

  if (response.data.errors) throw new Error(response.data.errors[0].message);
  return response.data.data;
};

export const fetchLeetCodeRecentSubmissions = async (username, limit = 15) => {
  const query = `
    query getRecentSubmissions($username: String!, $limit: Int) {
      recentSubmissionList(username: $username, limit: $limit) {
        id title titleSlug timestamp statusDisplay lang runtime memory
      }
    }
  `;

  const response = await api.post('/leetcode-proxy', { query, variables: { username, limit } });

  return response.data.data?.recentSubmissionList || [];
};
