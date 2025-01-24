document.getElementById('fetchButton').addEventListener('click', function() {
  // Get the current tab's URL
  chrome.tabs.query({ active: true, currentWindow: true }, function(tabs) {
      const currentTabUrl = tabs[0].url;

      // Ensure the URL is a valid LeetCode problem page
      if (currentTabUrl.includes("leetcode.com/problems/")) {
          // Get the selected language from the dropdown
          const selectedLanguage = document.getElementById('language').value;

          // Define the request payload
          const requestData = {
              problem_url: currentTabUrl,  // Automatically use the current URL
              file_type: selectedLanguage  // Use the selected language (py/cpp)
          };

          // Send the data to your Flask server
          fetch('http://127.0.0.1:5000/fetch', {
              method: 'POST',
              headers: {
                  'Content-Type': 'application/json'
              },
              body: JSON.stringify(requestData)
          })
          .then(response => response.json())
          .then(data => {
              if (data.message === "Success") {
                  alert('Problem fetched successfully!');
              } else {
                  alert('An error occurred: ' + data.error);
              }
          })
          .catch(error => {
              console.error('Error:', error);
              alert('Error occurred during request.');
          });
      } else {
          alert('Please open a valid LeetCode problem page.');
      }
  });
});
