import * as geometry from "./geometry"


describe("geometry.normalise()", () => {
    test("a", () => {
        expect(geometry.normalise({x: 5, y: 0})).toStrictEqual({x: 1, y: 0})
    })

    test("b", () => {
        expect(geometry.normalise({x: 0, y: -5})).toStrictEqual({x: 0, y: -1})
    })

    test("c", () => {
        expect(geometry.normalise({x: 3, y: 4})).toStrictEqual({x: 0.6, y: 0.8})
    })
})


describe("geometry.length()", () => {
    test("a", () => {
        expect(geometry.length({x: 5, y: 0})).toBe(5)
    })

    test("b", () => {
        expect(geometry.length({x: 0, y: -5})).toBe(5)
    })

    test("c", () => {
        expect(geometry.length({x: 3, y: 4})).toBe(5)
    })
})


describe("geometry.sub()", () => {
    test("a", () => {
        expect(geometry.sub({x: 5, y: 0}, {x: 20, y: 0})).toStrictEqual({x: -15, y: 0})
    })

    test("b", () => {
        expect(geometry.sub({x: 0, y: -5}, {x: -10, y: 5})).toStrictEqual({x: 10, y: -10})
    })

    test("c", () => {
        expect(geometry.sub({x: 3, y: 4}, {x: -2.5, y: -4})).toStrictEqual({x: 5.5, y: 8})
    })
})


describe("geometry.add()", () => {
    test("a", () => {
        expect(geometry.add({x: 5, y: 0}, {x: 20, y: 0})).toStrictEqual({x: 25, y: 0})
    })

    test("b", () => {
        expect(geometry.add({x: 0, y: -5}, {x: -10, y: 5})).toStrictEqual({x: -10, y: 0})
    })

    test("c", () => {
        expect(geometry.add({x: 3, y: 4}, {x: -2.5, y: -4})).toStrictEqual({x: 0.5, y: 0})
    })
})


describe("geometry.multiply()", () => {
    test("a", () => {
        expect(geometry.multiply({x: 5, y: 0}, 5)).toStrictEqual({x: 25, y: 0})
    })

    test("b", () => {
        expect(geometry.multiply({x: 0, y: -5}, 0.5)).toStrictEqual({x: 0, y: -2.5})
    })

    test("c", () => {
        expect(geometry.multiply({x: 3, y: 4}, -10)).toStrictEqual({x: -30, y: -40})
    })
})
