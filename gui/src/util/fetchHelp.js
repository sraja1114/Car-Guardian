const jsonHeader = { 'Content-Type': 'application/json', };

export async function fetchGet(url) {
    const response = await fetch(url, { headers: jsonHeader });
    const data = await response.json();
    return data;
};

export async function fetchPost(url, postData) {
    const response = await fetch(url, {
      method: 'POST',
      headers: jsonHeader,
      body: JSON.stringify(postData)
    });

    const data = await response.json();
    return data;
};