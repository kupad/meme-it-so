
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
        <div className="mt-5 md:mt-0 font-sttng-credits text-blue-sttng-credits">
            <h1 className="md:text-3xl word-spacing-xl">"{title}"</h1>
            <h2 className="md:text-lg">
                Season <span className="tracking-tighter">{getSeasonNum(ep)}</span> / Episode <span className="tracking-tighter">{getEpisodeNum(ep)}</span> <span className="tracking-tighter">({toTimeStr(ms)})</span>
            </h2>
        </div>
    );
}

export default Credits;
