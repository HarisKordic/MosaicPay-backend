export default class Helper {
	static transformURL(url: any) {
		return url.startsWith("https") ? url : `http://localhost:8000/${url}`;
	}
}
