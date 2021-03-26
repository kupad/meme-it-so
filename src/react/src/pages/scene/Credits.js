
const Credits = ({ep, title, ms}) => {

    /* Given S03E15 return 03 */
    const getSeasonNum = (ep) => {
        return ep.substring(1,3);
    }

    /* Given S03E15 return 15 */
    const getEpisodeNum = (ep) => {
        return ep.substring(4);
    }

    const toTimeStr = (ms) => {
        const totseconds = (ms / 1000);
        const m = Math.round(totseconds / 60);
        const s = Math.floor(totseconds % 60).toString().padStart(2,'0')
        return `${m}:${s}`;
    }

    return (
        <div className="font-sttng-credits text-blue-sttng-credits">
            <h1 className="text-3xl">"{title}"</h1>
            <h2 className="text-lg">Season {getSeasonNum(ep)} / Episode {getEpisodeNum(ep)} ({toTimeStr(ms)})</h2>
        </div>
    );
}

export default Credits;
