/*
This file is part of Meme It So

"Meme It So" is a media (TV show and movies) screen capture and text caption
database and image macro generator.
Copyright (C) 2021  Phillip Dreizen

Meme It So is free software: you can redistribute it and/or modify
it under the terms of the GNU Affero General Public License as published
by the Free Software Foundation, either version 3 of the License, or
(at your option) any later version.

Meme It So is distributed in the hope that it will be useful,
but WITHOUT ANY WARRANTY; without even the implied warranty of
MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
GNU Affero General Public License for more details.

You should have received a copy of the GNU Affero General Public License
along with this program.  If not, see <https://www.gnu.org/licenses/>.
*/

export const nframes = 6; //every nth frame

//given a frame, return ms offset
export function frame2ms (frame, fps) {
    return Math.round(frame / fps * 1000);
}

//given ms, return frame offset
export function ms2frame(ms, fps) {
    return Math.round(ms * fps / 1000);
}

/* take ms value as input and return a string of MM:SS */
export function toTimeStr(ms) {
    const totseconds = (ms / 1000);
    const m = Math.round(totseconds / 60);
    const s = Math.floor(totseconds % 60).toString().padStart(2,'0')
    return `${m}:${s}`;
}

/*
b64 encode string s using the URL and filesystem-safe alphabet, which substitutes - instead of + and _ instead of / in the standard Base64 alphabet,
*/
export function urlsafe_btoa(s) {
    return btoa(s).replace('+', '-').replace('/','_');
}

/* pad out a frame integer to 5. 1 -> 00001 */
export function padFrame(frame) {
    return frame.toString().padStart(5,'0')
}

/* Given S03E15 return S03 */
export function getSeason(ep) {
    return ep.substring(0,3);
}


export function staticImgUrl(ep, frame) {
    return `/static/thumbnails/${getSeason(ep)}/${ep}/${padFrame(frame)}.jpg`;
}
